const API_BASE = "https://omnipass-mu.vercel.app/generate";

const $ = (id) => document.getElementById(id);
const output = $("output");
const status = $("status");
const regenerateBtn = $("regenerate");
const copyBtn = $("copy");
const lengthInput = $("length");
const lengthDisplay = $("lengthDisplay");
const arabicCheck = $("arabic");
const arabicChip = $("arabicChip");
const charBreakdown = $("charBreakdown");
const latinCount = $("latinCount");
const arabicCount = $("arabicCount");
const numCount = $("numCount");
const symCount = $("symCount");
const strengthDisplay = $("strengthDisplay");

const SETTINGS_KEY = "omnipass_ext_settings";

let currentPassword = "";
let genPending = false;
let currentController = null;

function saveSettings() {
  localStorage.setItem(
    SETTINGS_KEY,
    JSON.stringify({
      length: parseInt(lengthInput.value),
      arabic: arabicCheck.checked,
    }),
  );
}

function loadSettings() {
  try {
    const raw = localStorage.getItem(SETTINGS_KEY);
    if (!raw) return;
    const s = JSON.parse(raw);
    if (s.length) lengthInput.value = s.length;
    arabicCheck.checked = s.arabic !== false;
  } catch {}
  arabicChip.classList.toggle("active", arabicCheck.checked);
}

function analyzePassword(pwd) {
  let latin = 0,
    arabic = 0,
    nums = 0,
    syms = 0;
  for (const ch of pwd) {
    const code = ch.codePointAt(0);
    if (code >= 0x0600 && code <= 0x06ff) {
      arabic++;
    } else if (/[a-zA-Z]/.test(ch)) {
      latin++;
    } else if (/[0-9]/.test(ch)) {
      nums++;
    } else {
      syms++;
    }
  }
  return { latin, arabic, nums, syms };
}

function colorizePassword(pwd) {
  let html = "";
  for (const ch of pwd) {
    const code = ch.codePointAt(0);
    if (code >= 0x0600 && code <= 0x06ff) {
      html += `<span class="ar-char">${ch}</span>`;
    } else if (/[a-zA-Z]/.test(ch)) {
      html += `<span class="latin-char">${ch}</span>`;
    } else if (/[0-9]/.test(ch)) {
      html += `<span class="num-char">${ch}</span>`;
    } else {
      html += `<span class="sym-char">${ch}</span>`;
    }
  }
  return html;
}

function getCharsetSize(ar) {
  let size = 26 + 26 + 10 + 32;
  if (ar) size += 48;
  return size;
}

function calcEntropy(length, cs) {
  return length * Math.log2(cs);
}

function getStrengthLabel(bits) {
  if (bits < 40) return { label: "Weak", cls: "weak" };
  if (bits < 60) return { label: "Fair", cls: "fair" };
  if (bits < 80) return { label: "Good", cls: "good" };
  if (bits < 100) return { label: "Strong", cls: "strong" };
  return { label: "Very Strong", cls: "very-strong" };
}

function updateSlider() {
  const val = lengthInput.value;
  const min = lengthInput.min || 8;
  const max = lengthInput.max || 128;
  const pct = ((val - min) / (max - min)) * 100;
  lengthInput.style.background = `linear-gradient(to right, var(--accent) ${pct}%, var(--border) ${pct}%)`;
  lengthDisplay.textContent = val;
}

let sliderTimeout;
lengthInput.addEventListener("input", () => {
  updateSlider();
  saveSettings();
  clearTimeout(sliderTimeout);
  sliderTimeout = setTimeout(generate, 150);
});
updateSlider();

function updateInfo(pwd) {
  const len = parseInt(lengthInput.value);
  const ar = arabicCheck.checked;
  const cs = getCharsetSize(ar);
  const bits = calcEntropy(len, cs);
  const strength = getStrengthLabel(bits);

  strengthDisplay.textContent = strength.label;
  strengthDisplay.className = "strength-tag " + strength.cls;

  const analysis = analyzePassword(pwd);
  latinCount.textContent = analysis.latin;
  arabicCount.textContent = analysis.arabic;
  numCount.textContent = analysis.nums;
  symCount.textContent = analysis.syms;
  charBreakdown.style.display = "flex";
}

async function generate() {
  // Cancel any previous in-flight request before starting a new one
  if (currentController) {
    currentController.abort();
  }
  currentController = new AbortController();
  const signal = currentController.signal;

  genPending = true;

  const len = parseInt(lengthInput.value);
  const ar = arabicCheck.checked;

  const params = new URLSearchParams({ length: len, include_arabic: ar });

  try {
    const res = await fetch(`${API_BASE}?${params}`, {
      signal,
      keepalive: true,
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    currentPassword = data.password;

    const pwdSpan = document.createElement("span");
    pwdSpan.className = "password-text";
    pwdSpan.innerHTML = colorizePassword(data.password);
    output.innerHTML = "";
    output.appendChild(pwdSpan);

    output.className = "password-display" + (ar ? " glow-warm" : " glow");
    updateInfo(data.password);
    status.textContent = "";
    status.className = "status";
  } catch (e) {
    if (e.name === "AbortError") return; // stale request — user already triggered a newer one
    output.innerHTML = '<span class="placeholder">Error</span>';
    output.className = "password-display";
    status.textContent = "Failed to reach API";
    status.className = "status error";
    charBreakdown.style.display = "none";
    strengthDisplay.textContent = "";
  } finally {
    genPending = false;
  }
}

function copy() {
  if (!currentPassword) return;
  navigator.clipboard.writeText(currentPassword).then(() => {
    status.textContent = "Copied!";
    status.className = "status success flash";
    copyBtn.classList.add("copied");
    copyBtn.innerHTML = '<span class="icon">&#10003;</span> Copied';
    setTimeout(() => {
      status.textContent = "";
      status.className = "status";
      copyBtn.classList.remove("copied");
      copyBtn.innerHTML = '<span class="icon">&#128203;</span> Copy';
    }, 2000);
  });
}

arabicCheck.addEventListener("change", () => {
  arabicChip.classList.toggle("active", arabicCheck.checked);
  saveSettings();
  generate();
});

regenerateBtn.addEventListener("click", generate);
copyBtn.addEventListener("click", copy);

loadSettings();
updateSlider();
generate();
