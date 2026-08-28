'use strict';

(() => {
  const CARD_SELECTOR = '.profile-card';
  const NICKNAME_SELECTOR = '[data-nkust-roster-nickname]';
  const ENHANCED_CLASS = 'nkust-roster-enhanced';
  const PHOTO_CLASS = 'nkust-roster-photo';

  let rosterByName = new Map();
  let scanQueued = false;

  function normalizeName(value) {
    return String(value || '')
      .normalize('NFKC')
      .replace(/\s+/gu, '')
      .trim();
  }

  function buildRosterIndex(roster) {
    const candidates = new Map();

    for (const person of roster) {
      const key = normalizeName(person.name);

      if (!key) {
        continue;
      }

      const sameName = candidates.get(key) || [];
      sameName.push(person);
      candidates.set(key, sameName);
    }

    const index = new Map();

    for (const [key, sameName] of candidates) {
      // 同名但資料不同時不自動套用，避免把照片放到錯的人身上。
      if (sameName.length === 1) {
        index.set(key, sameName[0]);
      }
    }

    return index;
  }

  function findCards() {
    const cards = new Set(document.querySelectorAll(CARD_SELECTOR));

    // 保留一個不依賴 class 名稱的後備路徑，網站小幅改版時仍可運作。
    for (const image of document.querySelectorAll('img[alt="Profile Picture"], img.profile')) {
      const card = image.closest(CARD_SELECTOR) || image.parentElement?.parentElement;

      if (card?.querySelector('.profile-info b, b')) {
        cards.add(card);
      }
    }

    return cards;
  }

  function ensureNickname(card, info, person) {
    let nickname = card.querySelector(NICKNAME_SELECTOR);
    const text = `綽號：${person.nickname}`;
    const title = `本機名單：${person.name}（${person.year}）`;
    const ariaLabel = `${person.name}的綽號是${person.nickname}`;

    if (!nickname) {
      nickname = document.createElement('span');
      nickname.className = 'nkust-roster-nickname';
      nickname.dataset.nkustRosterNickname = '';
      info.append(nickname);
    }

    if (nickname.textContent !== text) {
      nickname.textContent = text;
    }

    if (nickname.title !== title) {
      nickname.title = title;
    }

    if (nickname.getAttribute('aria-label') !== ariaLabel) {
      nickname.setAttribute('aria-label', ariaLabel);
    }
  }

  function ensurePhoto(card, image, person) {
    const photoUrl = new URL(chrome.runtime.getURL(person.photoPath)).href;

    if (image.dataset.nkustRosterPhoto === photoUrl && image.src === photoUrl) {
      return;
    }

    if (image.dataset.nkustRosterPhoto === photoUrl) {
      image.src = photoUrl;
      return;
    }

    if (image.dataset.nkustRosterPending === photoUrl) {
      return;
    }

    image.dataset.nkustRosterPending = photoUrl;
    const probe = new Image();

    probe.addEventListener('load', () => {
      const currentName = normalizeName(
        card.querySelector('.profile-info b, b')?.textContent
      );

      if (!image.isConnected || currentName !== normalizeName(person.name)) {
        return;
      }

      if (!image.dataset.nkustRosterOriginalSrc) {
        image.dataset.nkustRosterOriginalSrc = image.currentSrc || image.src;
      }

      image.removeAttribute('srcset');
      image.src = photoUrl;
      image.alt = `${person.name}（綽號：${person.nickname}）`;
      image.title = `${person.name}｜${person.nickname}`;
      image.classList.add(PHOTO_CLASS);
      image.dataset.nkustRosterPhoto = photoUrl;
      delete image.dataset.nkustRosterPending;
    }, { once: true });

    probe.addEventListener('error', () => {
      delete image.dataset.nkustRosterPending;
      console.warn(`[NKUST 通訊錄] 無法載入 ${person.photoPath}`);
    }, { once: true });

    probe.src = photoUrl;
  }

  function enhanceCard(card) {
    const nameNode = card.querySelector('.profile-info b, b');
    const info = card.querySelector('.profile-info') || nameNode?.parentElement;
    const image = card.querySelector('img.profile, img[alt="Profile Picture"]');

    if (!nameNode || !info || !image) {
      return false;
    }

    const person = rosterByName.get(normalizeName(nameNode.textContent));

    if (!person) {
      return false;
    }

    card.classList.add(ENHANCED_CLASS);
    card.dataset.nkustRosterName = person.name;
    ensureNickname(card, info, person);
    ensurePhoto(card, image, person);
    return true;
  }

  function scanDirectory() {
    scanQueued = false;

    if (!location.hash.includes('/learning/')) {
      return;
    }

    for (const card of findCards()) {
      enhanceCard(card);
    }
  }

  function queueScan() {
    if (scanQueued) {
      return;
    }

    scanQueued = true;
    queueMicrotask(scanDirectory);
  }

  async function start() {
    try {
      const response = await chrome.runtime.sendMessage({
        type: 'NKUST_GET_LOCAL_ROSTER'
      });

      if (!response?.ok || !Array.isArray(response.roster)) {
        throw new Error(response?.error || '名單回應格式不正確');
      }

      rosterByName = buildRosterIndex(response.roster);
      queueScan();

      const observer = new MutationObserver(queueScan);
      observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ['src'],
        childList: true,
        subtree: true
      });

      window.addEventListener('hashchange', queueScan);
      document.addEventListener('visibilitychange', () => {
        if (!document.hidden) {
          queueScan();
        }
      });
    } catch (error) {
      console.error('[NKUST 通訊錄] 載入本機名單失敗：', error);
    }
  }

  start();
})();
