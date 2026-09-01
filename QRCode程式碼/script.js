/*
 * QR 小工坊
 * A small, dependency-free QR Code encoder for byte-mode text.
 * The UI and renderer below are intentionally kept framework-free.
 */

(() => {
  "use strict";

  const refs = {
    form: document.querySelector("#qrForm"),
    urlInput: document.querySelector("#urlInput"),
    logoInput: document.querySelector("#logoInput"),
    logoThumb: document.querySelector("#logoThumb"),
    logoFileName: document.querySelector("#logoFileName"),
    logoControls: document.querySelector("#logoControls"),
    removeLogoButton: document.querySelector("#removeLogoButton"),
    formMessage: document.querySelector("#formMessage"),
    generateButton: document.querySelector("#generateButton"),
    clearButton: document.querySelector("#clearButton"),
    previewStatus: document.querySelector("#previewStatus"),
    previewStage: document.querySelector("#previewStage"),
    emptyState: document.querySelector("#emptyState"),
    qrCanvas: document.querySelector("#qrCanvas"),
    previewLogoBadge: document.querySelector("#previewLogoBadge"),
    resultInfo: document.querySelector("#resultInfo"),
    resultSettings: document.querySelector("#resultSettings"),
    resultUrl: document.querySelector("#resultUrl"),
    downloadButton: document.querySelector("#downloadButton"),
    downloadHint: document.querySelector("#downloadHint")
  };

  const state = {
    logoDataUrl: "",
    logoImage: null,
    logoFileName: "",
    hasGenerated: false,
    isGenerating: false
  };

  const OUTPUT_SIZES = {
    500: "500 × 500 px",
    800: "800 × 800 px",
    1000: "1000 × 1000 px"
  };

  const ERROR_LABELS = {
    L: "低",
    M: "中",
    H: "高"
  };

  const LOGO_RATIOS = {
    S: 0.16,
    M: 0.23,
    L: 0.30
  };

  const LOGO_LABELS = {
    S: "小",
    M: "中",
    L: "大"
  };

  function getCheckedValue(name) {
    const input = document.querySelector(`input[name="${name}"]:checked`);
    return input ? input.value : "";
  }

  function syncChoiceCards() {
    document.querySelectorAll(".choice-card").forEach((card) => {
      const input = card.querySelector("input");
      card.classList.toggle("selected", Boolean(input && input.checked));
    });
  }

  function setMessage(message, type = "") {
    refs.formMessage.textContent = message;
    refs.formMessage.classList.toggle("is-error", type === "error");
    refs.formMessage.setAttribute("aria-live", type === "error" ? "assertive" : "polite");
  }

  function normaliseUrl(rawValue) {
    const raw = rawValue.trim();

    if (!raw) {
      return { error: "先貼上一個網址，再來畫 QR Code 喔！" };
    }

    if (/\s/.test(raw)) {
      return { error: "網址裡有空白，請刪掉空白後再試一次。" };
    }

    let candidate = raw;
    if (!/^[a-z][a-z\d+.-]*:\/\//i.test(candidate)) {
      candidate = `https://${candidate}`;
    }

    try {
      const parsed = new URL(candidate);
      if (!["http:", "https:"].includes(parsed.protocol) || !parsed.hostname) {
        return { error: "目前只接受 http:// 或 https:// 開頭的網址。" };
      }
      return { value: parsed.toString() };
    } catch (error) {
      return { error: "這個網址好像少了一點東西，請檢查後再試一次。" };
    }
  }

  function readFileAsDataUrl(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.addEventListener("load", () => resolve(String(reader.result)));
      reader.addEventListener("error", () => reject(new Error("檔案讀取失敗")));
      reader.readAsDataURL(file);
    });
  }

  function loadImage(dataUrl) {
    return new Promise((resolve, reject) => {
      const image = new Image();
      image.addEventListener("load", () => resolve(image));
      image.addEventListener("error", () => reject(new Error("這張圖片無法載入")));
      image.src = dataUrl;
    });
  }

  function resetLogo() {
    state.logoDataUrl = "";
    state.logoImage = null;
    state.logoFileName = "";
    refs.logoInput.value = "";
    refs.logoThumb.src = "";
    refs.logoThumb.hidden = true;
    refs.logoFileName.textContent = "";
    refs.logoFileName.hidden = true;
    refs.logoControls.hidden = true;
    refs.logoInput.closest(".upload-box").classList.remove("has-logo");
  }

  async function handleLogoUpload(event) {
    const file = event.target.files && event.target.files[0];
    if (!file) return;

    if (file.size > 5 * 1024 * 1024) {
      resetLogo();
      setMessage("這張圖超過 5 MB，換一張輕一點的 Logo 吧。", "error");
      return;
    }

    if (!file.type.startsWith("image/")) {
      resetLogo();
      setMessage("這個檔案不是圖片，請選 PNG、JPG 或 WEBP。", "error");
      return;
    }

    try {
      const dataUrl = await readFileAsDataUrl(file);
      const image = await loadImage(dataUrl);

      state.logoDataUrl = dataUrl;
      state.logoImage = image;
      state.logoFileName = file.name;
      refs.logoThumb.src = dataUrl;
      refs.logoThumb.hidden = false;
      refs.logoFileName.textContent = file.name;
      refs.logoFileName.hidden = false;
      refs.logoControls.hidden = false;
      refs.logoInput.closest(".upload-box").classList.add("has-logo");
      setMessage(`已放入 ${file.name}，準備好就按產生！`);
    } catch (error) {
      resetLogo();
      setMessage("圖片讀取失敗，請換一張圖片再試一次。", "error");
    }
  }

  function roundedRectPath(context, x, y, width, height, radius) {
    const r = Math.min(radius, width / 2, height / 2);
    context.beginPath();
    context.moveTo(x + r, y);
    context.arcTo(x + width, y, x + width, y + height, r);
    context.arcTo(x + width, y + height, x, y + height, r);
    context.arcTo(x, y + height, x, y, r);
    context.arcTo(x, y, x + width, y, r);
    context.closePath();
  }

  function drawLogo(context, image, canvasSize, logoSizeKey) {
    const imageSize = Math.round(canvasSize * (LOGO_RATIOS[logoSizeKey] || LOGO_RATIOS.M));
    const outerSize = Math.round(imageSize * 1.28);
    const outerX = Math.round((canvasSize - outerSize) / 2);
    const outerY = Math.round((canvasSize - outerSize) / 2);
    const corner = Math.max(12, Math.round(outerSize * 0.105));
    const borderWidth = Math.max(3, Math.round(canvasSize / 265));
    const innerPadding = Math.max(8, Math.round(outerSize * 0.10));
    const innerSize = outerSize - innerPadding * 2;
    const ratio = Math.min(innerSize / image.naturalWidth, innerSize / image.naturalHeight);
    const drawWidth = Math.max(1, Math.round(image.naturalWidth * ratio));
    const drawHeight = Math.max(1, Math.round(image.naturalHeight * ratio));
    const drawX = Math.round((canvasSize - drawWidth) / 2);
    const drawY = Math.round((canvasSize - drawHeight) / 2);

    context.save();
    context.imageSmoothingEnabled = true;
    roundedRectPath(context, outerX, outerY, outerSize, outerSize, corner);
    context.fillStyle = "#ffffff";
    context.fill();
    context.lineWidth = borderWidth;
    context.strokeStyle = "#111111";
    context.stroke();

    roundedRectPath(
      context,
      outerX + innerPadding,
      outerY + innerPadding,
      innerSize,
      innerSize,
      Math.max(7, corner - innerPadding)
    );
    context.clip();
    context.drawImage(image, drawX, drawY, drawWidth, drawHeight);
    context.restore();
  }

  function renderQrCanvas(canvas, qr, outputSize, logoImage, logoSizeKey) {
    canvas.width = outputSize;
    canvas.height = outputSize;

    const context = canvas.getContext("2d", { alpha: false });
    const quietZone = 4;
    const units = qr.moduleCount + quietZone * 2;
    const moduleSize = outputSize / units;

    context.imageSmoothingEnabled = false;
    context.fillStyle = "#ffffff";
    context.fillRect(0, 0, outputSize, outputSize);
    context.fillStyle = "#111111";

    for (let row = 0; row < qr.moduleCount; row += 1) {
      for (let column = 0; column < qr.moduleCount; column += 1) {
        if (!qr.modules[row][column]) continue;
        const x = Math.floor((column + quietZone) * moduleSize);
        const y = Math.floor((row + quietZone) * moduleSize);
        const nextX = Math.ceil((column + quietZone + 1) * moduleSize);
        const nextY = Math.ceil((row + quietZone + 1) * moduleSize);
        context.fillRect(x, y, nextX - x, nextY - y);
      }
    }

    if (logoImage) {
      drawLogo(context, logoImage, outputSize, logoSizeKey);
    }
  }

  function setGenerating(isGenerating) {
    state.isGenerating = isGenerating;
    refs.generateButton.disabled = isGenerating;
    refs.generateButton.innerHTML = isGenerating
      ? "<span aria-hidden=\"true\">…</span> 正在畫圖"
      : "<span aria-hidden=\"true\">✎</span> 產生 QR Code";
  }

  async function generateQr() {
    if (state.isGenerating) return;

    const normalised = normaliseUrl(refs.urlInput.value);
    refs.urlInput.classList.toggle("is-invalid", Boolean(normalised.error));

    if (normalised.error) {
      setMessage(normalised.error, "error");
      refs.urlInput.focus();
      return;
    }

    const url = normalised.value;
    const outputSize = Number(getCheckedValue("outputSize") || 800);
    const errorLevel = getCheckedValue("errorLevel") || "M";
    const logoSize = getCheckedValue("logoSize") || "M";

    refs.urlInput.value = url;
    setGenerating(true);
    setMessage("正在把網址排成一格一格，等我一下～");

    try {
      const qr = QrCodeEncoder.encode(url, errorLevel);
      renderQrCanvas(refs.qrCanvas, qr, outputSize, state.logoImage, logoSize);

      refs.emptyState.hidden = true;
      refs.qrCanvas.hidden = false;
      refs.previewLogoBadge.hidden = !state.logoImage;
      refs.resultInfo.hidden = false;
      refs.resultSettings.textContent = `${OUTPUT_SIZES[outputSize]} ・ ${ERROR_LABELS[errorLevel]}容錯${state.logoImage ? ` ・ Logo${LOGO_LABELS[logoSize]}` : ""}`;
      refs.resultUrl.textContent = url;
      refs.previewStatus.textContent = "畫好了！";
      refs.previewStatus.classList.add("is-ready");
      refs.downloadButton.disabled = false;
      refs.downloadHint.textContent = "黑白小方塊已完成，按下面把 PNG 帶走！";
      refs.urlInput.classList.remove("is-invalid");
      state.hasGenerated = true;
      setMessage(state.logoImage ? "完成！Logo 也乖乖待在中間了。" : "完成！你的 QR Code 出現了！");
    } catch (error) {
      state.hasGenerated = false;
      setMessage(error instanceof Error ? error.message : "QR Code 產生失敗，請換一個網址再試。", "error");
    } finally {
      setGenerating(false);
    }
  }

  function downloadQr() {
    if (!state.hasGenerated || refs.downloadButton.disabled) return;

    refs.qrCanvas.toBlob((blob) => {
      if (!blob) {
        setMessage("圖檔準備失敗，請再按一次下載。", "error");
        return;
      }

      const link = document.createElement("a");
      const stamp = new Date().toISOString().slice(0, 10).replaceAll("-", "");
      const outputSize = getCheckedValue("outputSize") || "800";
      const downloadUrl = URL.createObjectURL(blob);
      link.href = downloadUrl;
      link.download = `qr-code-${outputSize}-${stamp}.png`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.setTimeout(() => URL.revokeObjectURL(downloadUrl), 1000);
      refs.downloadHint.textContent = "下載開始囉！再畫一張也可以～";
    }, "image/png");
  }

  function clearAll() {
    refs.form.reset();
    syncChoiceCards();
    resetLogo();
    state.hasGenerated = false;
    refs.urlInput.classList.remove("is-invalid");
    refs.emptyState.hidden = false;
    refs.qrCanvas.hidden = true;
    refs.qrCanvas.width = 1;
    refs.qrCanvas.height = 1;
    refs.previewLogoBadge.hidden = true;
    refs.resultInfo.hidden = true;
    refs.previewStatus.textContent = "還沒開始";
    refs.previewStatus.classList.remove("is-ready");
    refs.downloadButton.disabled = true;
    refs.downloadHint.textContent = "完成後就可以把它帶走囉！";
    setMessage("全部擦乾淨了，想畫新的就再貼一個網址吧～");
  }

  refs.form.addEventListener("submit", (event) => {
    event.preventDefault();
    void generateQr();
  });

  refs.logoInput.addEventListener("change", (event) => {
    void handleLogoUpload(event);
  });

  refs.removeLogoButton.addEventListener("click", () => {
    resetLogo();
    setMessage(state.hasGenerated ? "Logo 已移除；按「產生 QR Code」就會更新成果。" : "Logo 已移除。 ");
  });

  refs.clearButton.addEventListener("click", clearAll);
  refs.downloadButton.addEventListener("click", downloadQr);

  document.querySelectorAll("input[type=radio]").forEach((input) => {
    input.addEventListener("change", () => {
      syncChoiceCards();
      if (state.hasGenerated) {
        setMessage("設定變更了，按「產生 QR Code」套用新的樣子吧～");
      }
    });
  });

  syncChoiceCards();

  /* ------------------------- QR Code encoder ------------------------- */

  const ERROR_CORRECTION_FORMAT = {
    L: 1,
    M: 0,
    Q: 3,
    H: 2
  };

  // Versions 1–10 cover normal URLs while keeping this project small and readable.
  // Each tuple is [number of blocks, total codewords per block, data codewords per block].
  const RS_BLOCK_TABLE = {
    1: {
      L: [[1, 26, 19]],
      M: [[1, 26, 16]],
      Q: [[1, 26, 13]],
      H: [[1, 26, 9]]
    },
    2: {
      L: [[1, 44, 34]],
      M: [[1, 44, 28]],
      Q: [[1, 44, 22]],
      H: [[1, 44, 16]]
    },
    3: {
      L: [[1, 70, 55]],
      M: [[1, 70, 44]],
      Q: [[2, 35, 17]],
      H: [[2, 35, 13]]
    },
    4: {
      L: [[1, 100, 80]],
      M: [[2, 50, 32]],
      Q: [[2, 50, 24]],
      H: [[4, 25, 9]]
    },
    5: {
      L: [[1, 134, 108]],
      M: [[2, 67, 43]],
      Q: [[2, 33, 15], [2, 34, 16]],
      H: [[2, 33, 11], [2, 34, 12]]
    },
    6: {
      L: [[2, 86, 68]],
      M: [[4, 43, 27]],
      Q: [[4, 43, 19]],
      H: [[4, 43, 15]]
    },
    7: {
      L: [[2, 98, 78]],
      M: [[4, 49, 31]],
      Q: [[2, 32, 14], [4, 33, 15]],
      H: [[4, 39, 13], [1, 40, 14]]
    },
    8: {
      L: [[2, 121, 97]],
      M: [[2, 60, 38], [2, 61, 39]],
      Q: [[4, 40, 18], [2, 41, 19]],
      H: [[4, 40, 14], [2, 41, 15]]
    },
    9: {
      L: [[2, 146, 116]],
      M: [[3, 58, 36], [2, 59, 37]],
      Q: [[4, 36, 16], [4, 37, 17]],
      H: [[4, 36, 12], [4, 37, 13]]
    },
    10: {
      L: [[2, 86, 68], [2, 87, 69]],
      M: [[4, 69, 43], [1, 70, 44]],
      Q: [[6, 43, 19], [2, 44, 20]],
      H: [[6, 43, 15], [2, 44, 16]]
    }
  };

  const ALIGNMENT_PATTERN_POSITIONS = {
    1: [],
    2: [6, 18],
    3: [6, 22],
    4: [6, 26],
    5: [6, 30],
    6: [6, 34],
    7: [6, 22, 38],
    8: [6, 24, 42],
    9: [6, 26, 46],
    10: [6, 28, 50]
  };

  const GF_EXP = new Array(256);
  const GF_LOG = new Array(256);
  GF_EXP[0] = 1;
  for (let i = 1; i < 256; i += 1) {
    let value = GF_EXP[i - 1] << 1;
    if (value & 0x100) value ^= 0x11d;
    GF_EXP[i] = value;
  }
  for (let i = 0; i < 255; i += 1) {
    GF_LOG[GF_EXP[i]] = i;
  }

  function gfExp(value) {
    let index = value;
    while (index < 0) index += 255;
    while (index >= 255) index -= 255;
    return GF_EXP[index];
  }

  function gfLog(value) {
    if (value === 0) throw new Error("GF(256) log(0) is undefined");
    return GF_LOG[value];
  }

  class Polynomial {
    constructor(coefficients, shift = 0) {
      let offset = 0;
      while (offset < coefficients.length && coefficients[offset] === 0) offset += 1;
      this.coefficients = coefficients.slice(offset).concat(new Array(shift).fill(0));
      if (this.coefficients.length === 0) this.coefficients = [0];
    }

    get length() {
      return this.coefficients.length;
    }

    get(index) {
      return index >= 0 && index < this.coefficients.length ? this.coefficients[index] : 0;
    }

    multiply(other) {
      const result = new Array(this.length + other.length - 1).fill(0);
      for (let i = 0; i < this.length; i += 1) {
        if (this.get(i) === 0) continue;
        for (let j = 0; j < other.length; j += 1) {
          if (other.get(j) === 0) continue;
          result[i + j] ^= gfExp(gfLog(this.get(i)) + gfLog(other.get(j)));
        }
      }
      return new Polynomial(result, 0);
    }

    mod(other) {
      if (this.length < other.length) return this;

      const result = this.coefficients.slice();
      const ratio = gfLog(result[0]) - gfLog(other.get(0));
      for (let i = 0; i < other.length; i += 1) {
        if (other.get(i) !== 0) {
          result[i] ^= gfExp(gfLog(other.get(i)) + ratio);
        }
      }
      return new Polynomial(result, 0).mod(other);
    }
  }

  function getGeneratorPolynomial(errorCodewords) {
    let polynomial = new Polynomial([1], 0);
    for (let i = 0; i < errorCodewords; i += 1) {
      polynomial = polynomial.multiply(new Polynomial([1, gfExp(i)], 0));
    }
    return polynomial;
  }

  class BitBuffer {
    constructor() {
      this.buffer = [];
      this.length = 0;
    }

    put(value, length) {
      for (let i = 0; i < length; i += 1) {
        this.putBit(((value >>> (length - i - 1)) & 1) === 1);
      }
    }

    putBit(bit) {
      const index = Math.floor(this.length / 8);
      if (this.buffer.length <= index) this.buffer.push(0);
      if (bit) this.buffer[index] |= 0x80 >>> (this.length % 8);
      this.length += 1;
    }
  }

  function getUtf8Bytes(text) {
    if (typeof TextEncoder !== "undefined") {
      return Array.from(new TextEncoder().encode(text));
    }

    const encoded = unescape(encodeURIComponent(text));
    return Array.from(encoded, (character) => character.charCodeAt(0));
  }

  function getRsBlocks(version, errorLevel) {
    const groups = RS_BLOCK_TABLE[version] && RS_BLOCK_TABLE[version][errorLevel];
    if (!groups) throw new Error("這個網址太長了，請縮短後再試一次。 ");

    const blocks = [];
    groups.forEach(([count, totalCount, dataCount]) => {
      for (let i = 0; i < count; i += 1) {
        blocks.push({ totalCount, dataCount });
      }
    });
    return blocks;
  }

  function buildDataBytes(version, errorLevel, bytes, blocks) {
    const totalDataCount = blocks.reduce((sum, block) => sum + block.dataCount, 0);
    const buffer = new BitBuffer();
    const characterCountBits = version < 10 ? 8 : 16;

    buffer.put(0b0100, 4);
    buffer.put(bytes.length, characterCountBits);
    bytes.forEach((byte) => buffer.put(byte, 8));

    if (buffer.length > totalDataCount * 8) {
      throw new Error("這個網址太長了，請縮短後再試一次。 ");
    }

    for (let i = 0; i < Math.min(4, totalDataCount * 8 - buffer.length); i += 1) {
      buffer.putBit(false);
    }
    while (buffer.length % 8 !== 0) buffer.putBit(false);

    let padByte = 0xec;
    while (buffer.buffer.length < totalDataCount) {
      buffer.put(padByte, 8);
      padByte = padByte === 0xec ? 0x11 : 0xec;
    }

    const dataBlocks = [];
    const errorBlocks = [];
    let offset = 0;

    blocks.forEach((block) => {
      const data = buffer.buffer.slice(offset, offset + block.dataCount);
      offset += block.dataCount;
      const errorCount = block.totalCount - block.dataCount;
      const rawPolynomial = new Polynomial(data, errorCount);
      const generator = getGeneratorPolynomial(errorCount);
      const remainder = rawPolynomial.mod(generator);
      const error = new Array(errorCount).fill(0);

      for (let i = 0; i < errorCount; i += 1) {
        const remainderIndex = i + remainder.length - errorCount;
        error[i] = remainderIndex >= 0 ? remainder.get(remainderIndex) : 0;
      }

      dataBlocks.push(data);
      errorBlocks.push(error);
    });

    const interleaved = [];
    const maxDataLength = Math.max(...dataBlocks.map((block) => block.length));
    const maxErrorLength = Math.max(...errorBlocks.map((block) => block.length));

    for (let i = 0; i < maxDataLength; i += 1) {
      dataBlocks.forEach((block) => {
        if (i < block.length) interleaved.push(block[i]);
      });
    }
    for (let i = 0; i < maxErrorLength; i += 1) {
      errorBlocks.forEach((block) => {
        if (i < block.length) interleaved.push(block[i]);
      });
    }

    return interleaved;
  }

  function getBchDigit(data) {
    let digit = 0;
    let value = data;
    while (value !== 0) {
      digit += 1;
      value >>>= 1;
    }
    return digit;
  }

  function getBchTypeInfo(data) {
    const generator = 0x537;
    const mask = 0x5412;
    let value = data << 10;
    while (getBchDigit(value) - getBchDigit(generator) >= 0) {
      value ^= generator << (getBchDigit(value) - getBchDigit(generator));
    }
    return ((data << 10) | value) ^ mask;
  }

  function getBchTypeNumber(version) {
    const generator = 0x1f25;
    let value = version << 12;
    while (getBchDigit(value) - getBchDigit(generator) >= 0) {
      value ^= generator << (getBchDigit(value) - getBchDigit(generator));
    }
    return (version << 12) | value;
  }

  function setupFinderPattern(modules, row, column) {
    const moduleCount = modules.length;
    for (let r = -1; r <= 7; r += 1) {
      if (row + r < 0 || moduleCount <= row + r) continue;
      for (let c = -1; c <= 7; c += 1) {
        if (column + c < 0 || moduleCount <= column + c) continue;
        const isBorder = (r >= 0 && r <= 6 && (c === 0 || c === 6)) ||
          (c >= 0 && c <= 6 && (r === 0 || r === 6));
        const isCenter = r >= 2 && r <= 4 && c >= 2 && c <= 4;
        modules[row + r][column + c] = isBorder || isCenter;
      }
    }
  }

  function setupAlignmentPatterns(modules, version) {
    const positions = ALIGNMENT_PATTERN_POSITIONS[version] || [];
    for (const row of positions) {
      for (const column of positions) {
        if (modules[row][column] !== null) continue;
        for (let r = -2; r <= 2; r += 1) {
          for (let c = -2; c <= 2; c += 1) {
            modules[row + r][column + c] = Math.max(Math.abs(r), Math.abs(c)) !== 1;
          }
        }
      }
    }
  }

  function setupTimingPatterns(modules) {
    const moduleCount = modules.length;
    for (let i = 8; i < moduleCount - 8; i += 1) {
      if (modules[i][6] === null) modules[i][6] = i % 2 === 0;
      if (modules[6][i] === null) modules[6][i] = i % 2 === 0;
    }
  }

  function setupTypeInfo(modules, errorLevel, maskPattern, test) {
    const moduleCount = modules.length;
    const bits = getBchTypeInfo((ERROR_CORRECTION_FORMAT[errorLevel] << 3) | maskPattern);

    for (let i = 0; i < 15; i += 1) {
      const bit = !test && ((bits >>> i) & 1) === 1;
      if (i < 6) modules[i][8] = bit;
      else if (i < 8) modules[i + 1][8] = bit;
      else modules[moduleCount - 15 + i][8] = bit;
    }

    for (let i = 0; i < 15; i += 1) {
      const bit = !test && ((bits >>> i) & 1) === 1;
      if (i < 8) modules[8][moduleCount - i - 1] = bit;
      else if (i < 9) modules[8][15 - i - 1 + 1] = bit;
      else modules[8][15 - i - 1] = bit;
    }

    modules[moduleCount - 8][8] = !test;
  }

  function setupTypeNumber(modules, version, test) {
    const moduleCount = modules.length;
    const bits = getBchTypeNumber(version);
    for (let i = 0; i < 18; i += 1) {
      const bit = !test && ((bits >>> i) & 1) === 1;
      modules[Math.floor(i / 3)][i % 3 + moduleCount - 8 - 3] = bit;
      modules[i % 3 + moduleCount - 8 - 3][Math.floor(i / 3)] = bit;
    }
  }

  function maskApplies(maskPattern, row, column) {
    switch (maskPattern) {
      case 0: return (row + column) % 2 === 0;
      case 1: return row % 2 === 0;
      case 2: return column % 3 === 0;
      case 3: return (row + column) % 3 === 0;
      case 4: return (Math.floor(row / 2) + Math.floor(column / 3)) % 2 === 0;
      case 5: return (row * column) % 2 + (row * column) % 3 === 0;
      case 6: return ((row * column) % 2 + (row * column) % 3) % 2 === 0;
      case 7: return ((row * column) % 3 + (row + column) % 2) % 2 === 0;
      default: return false;
    }
  }

  function mapData(modules, data, maskPattern) {
    const moduleCount = modules.length;
    let direction = -1;
    let row = moduleCount - 1;
    let bitIndex = 7;
    let byteIndex = 0;

    for (let column = moduleCount - 1; column > 0; column -= 2) {
      if (column === 6) column -= 1;

      while (true) {
        for (let offset = 0; offset < 2; offset += 1) {
          const currentColumn = column - offset;
          if (modules[row][currentColumn] !== null) continue;

          let dark = false;
          if (byteIndex < data.length) {
            dark = ((data[byteIndex] >>> bitIndex) & 1) === 1;
          }
          if (maskApplies(maskPattern, row, currentColumn)) dark = !dark;
          modules[row][currentColumn] = dark;
          bitIndex -= 1;
          if (bitIndex === -1) {
            byteIndex += 1;
            bitIndex = 7;
          }
        }

        row += direction;
        if (row < 0 || moduleCount <= row) {
          row -= direction;
          direction = -direction;
          break;
        }
      }
    }
  }

  function buildMatrix(version, errorLevel, data, maskPattern, test = false) {
    const moduleCount = version * 4 + 17;
    const modules = Array.from({ length: moduleCount }, () => new Array(moduleCount).fill(null));

    setupFinderPattern(modules, 0, 0);
    setupFinderPattern(modules, moduleCount - 7, 0);
    setupFinderPattern(modules, 0, moduleCount - 7);
    setupAlignmentPatterns(modules, version);
    setupTimingPatterns(modules);
    setupTypeInfo(modules, errorLevel, maskPattern, test);
    if (version >= 7) setupTypeNumber(modules, version, test);
    mapData(modules, data, maskPattern);

    return modules;
  }

  function getLostPoint(modules) {
    const moduleCount = modules.length;
    let lostPoint = 0;

    for (let row = 0; row < moduleCount; row += 1) {
      for (let column = 0; column < moduleCount; column += 1) {
        let sameCount = 0;
        const dark = modules[row][column];
        for (let r = -1; r <= 1; r += 1) {
          if (row + r < 0 || moduleCount <= row + r) continue;
          for (let c = -1; c <= 1; c += 1) {
            if (column + c < 0 || moduleCount <= column + c) continue;
            if (r === 0 && c === 0) continue;
            if (dark === modules[row + r][column + c]) sameCount += 1;
          }
        }
        if (sameCount > 5) lostPoint += 3 + sameCount - 5;
      }
    }

    for (let row = 0; row < moduleCount - 1; row += 1) {
      for (let column = 0; column < moduleCount - 1; column += 1) {
        const count = Number(modules[row][column]) +
          Number(modules[row + 1][column]) +
          Number(modules[row][column + 1]) +
          Number(modules[row + 1][column + 1]);
        if (count === 0 || count === 4) lostPoint += 3;
      }
    }

    for (let row = 0; row < moduleCount; row += 1) {
      for (let column = 0; column < moduleCount - 6; column += 1) {
        if (modules[row][column] &&
          !modules[row][column + 1] &&
          modules[row][column + 2] &&
          modules[row][column + 3] &&
          modules[row][column + 4] &&
          !modules[row][column + 5] &&
          modules[row][column + 6]) {
          lostPoint += 40;
        }
      }
    }

    for (let column = 0; column < moduleCount; column += 1) {
      for (let row = 0; row < moduleCount - 6; row += 1) {
        if (modules[row][column] &&
          !modules[row + 1][column] &&
          modules[row + 2][column] &&
          modules[row + 3][column] &&
          modules[row + 4][column] &&
          !modules[row + 5][column] &&
          modules[row + 6][column]) {
          lostPoint += 40;
        }
      }
    }

    let darkCount = 0;
    modules.forEach((row) => row.forEach((module) => {
      if (module) darkCount += 1;
    }));
    const ratio = Math.abs((100 * darkCount) / (moduleCount * moduleCount) - 50) / 5;
    lostPoint += ratio * 10;
    return lostPoint;
  }

  const QrCodeEncoder = {
    encode(text, errorLevel = "M") {
      const bytes = getUtf8Bytes(text);
      let selectedVersion = 0;
      let selectedBlocks = null;

      for (let version = 1; version <= 10; version += 1) {
        const blocks = getRsBlocks(version, errorLevel);
        const capacity = blocks.reduce((sum, block) => sum + block.dataCount, 0) * 8;
        const countBits = version < 10 ? 8 : 16;
        const required = 4 + countBits + bytes.length * 8;
        if (required <= capacity) {
          selectedVersion = version;
          selectedBlocks = blocks;
          break;
        }
      }

      if (!selectedVersion || !selectedBlocks) {
        throw new Error("這個網址太長了，請縮短後再試一次。 ");
      }

      const data = buildDataBytes(selectedVersion, errorLevel, bytes, selectedBlocks);
      let bestModules = null;
      let bestLostPoint = Number.POSITIVE_INFINITY;

      for (let maskPattern = 0; maskPattern < 8; maskPattern += 1) {
        const modules = buildMatrix(selectedVersion, errorLevel, data, maskPattern);
        const lostPoint = getLostPoint(modules);
        if (lostPoint < bestLostPoint) {
          bestLostPoint = lostPoint;
          bestModules = modules;
        }
      }

      return {
        version: selectedVersion,
        moduleCount: selectedVersion * 4 + 17,
        modules: bestModules
      };
    }
  };
})();
