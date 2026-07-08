const API_BASE = "https://omnipass-mu.vercel.app/generate";
const output = document.getElementById("output");
const status = document.getElementById("status");
const generateBtn = document.getElementById("generate");
const copyBtn = document.getElementById("copy");
const lengthInput = document.getElementById("length");
const arabicCheck = document.getElementById("arabic");
const numbersCheck = document.getElementById("numbers");

async function generate() {
  const len = lengthInput.value || 16;
  const ar = arabicCheck.checked;
  const nums = numbersCheck.checked;

  const params = new URLSearchParams({
    length: len,
    include_arabic: ar,
    include_numbers: nums,
  });

  try {
    const res = await fetch(`${API_BASE}?${params}`);
    const data = await res.json();
    output.textContent = data.password;
    status.textContent = "";
  } catch (e) {
    output.textContent = "Error";
    status.textContent = "Failed";
  }
}

function copy() {
  const pwd = output.textContent;
  if (pwd && pwd !== "Generate" && pwd !== "Error") {
    navigator.clipboard.writeText(pwd).then(() => {
      status.textContent = "Copied!";
      status.classList.add("ok");
      setTimeout(() => {
        status.textContent = "";
        status.classList.remove("ok");
      }, 1500);
    });
  }
}

generateBtn.addEventListener("click", generate);
copyBtn.addEventListener("click", copy);
lengthInput.addEventListener(
  "keypress",
  (e) => e.key === "Enter" && generate(),
);

generate();
