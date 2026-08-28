'use strict';

const ROSTER_FILES = Object.freeze([
  Object.freeze({ year: '114', path: '114/114名單簡單.json' }),
  Object.freeze({ year: '115', path: '115/115名單簡單.json' })
]);

let rosterPromise;

function isNonEmptyString(value) {
  return typeof value === 'string' && value.trim().length > 0;
}

function isAllowedSender(sender) {
  const senderUrl = sender.url || sender.tab?.url;

  if (!senderUrl) {
    return false;
  }

  try {
    const url = new URL(senderUrl);
    return url.protocol === 'https:'
      && url.hostname === 'elearning.nkust.edu.tw'
      && url.pathname.startsWith('/moocs/');
  } catch {
    return false;
  }
}

async function readRosterFile(file) {
  const response = await fetch(chrome.runtime.getURL(file.path));

  if (!response.ok) {
    throw new Error(`無法讀取 ${file.path} (${response.status})`);
  }

  const rows = await response.json();

  if (!Array.isArray(rows)) {
    throw new Error(`${file.path} 的最外層必須是陣列`);
  }

  return rows.map((row, index) => {
    if (!row || typeof row !== 'object') {
      throw new Error(`${file.path} 第 ${index + 1} 筆不是物件`);
    }

    const name = row['姓名'];
    const nickname = row['綽號'];
    const photo = row['照片'];

    if (![name, nickname, photo].every(isNonEmptyString)) {
      throw new Error(`${file.path} 第 ${index + 1} 筆缺少姓名、綽號或照片`);
    }

    return {
      name: name.trim(),
      nickname: nickname.trim(),
      photoPath: `${file.year}/${photo.trim()}`,
      year: file.year
    };
  });
}

async function loadRoster() {
  const groups = await Promise.all(ROSTER_FILES.map(readRosterFile));
  return groups.flat();
}

function getRoster() {
  rosterPromise ||= loadRoster().catch((error) => {
    rosterPromise = undefined;
    throw error;
  });

  return rosterPromise;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message?.type !== 'NKUST_GET_LOCAL_ROSTER' || !isAllowedSender(sender)) {
    return false;
  }

  getRoster()
    .then((roster) => sendResponse({ ok: true, roster }))
    .catch((error) => sendResponse({ ok: false, error: error.message }));

  return true;
});
