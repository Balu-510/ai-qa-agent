const form = document.getElementById("instruction-form");
const textarea = document.getElementById("instruction");
const gutter = document.getElementById("gutter");
const consoleEl = document.getElementById("console");
const statusTag = document.getElementById("status-tag");
const runBtn = document.querySelector(".run-btn");

const BADGE_CLASS = {
  open: "badge-open",
  click: "badge-click",
  username: "badge-username",
  password: "badge-password",
  unknown: "badge-unknown",
};

const STEP_DELAY_MS = 220;

function updateGutter() {
  const lineCount = textarea.value.split("\n").length;
  const total = Math.max(lineCount, 1);
  let html = "";
  for (let i = 1; i <= total; i++) {
    html += `<span>${i}</span>`;
  }
  gutter.innerHTML = html;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function formatTime(ms) {
  const totalSeconds = ms / 1000;
  return `00:${totalSeconds.toFixed(2).padStart(5, "0")}`;
}

function setStatus(text, variant) {
  statusTag.textContent = text;
  statusTag.classList.remove("tag-running", "tag-done");
  if (variant) statusTag.classList.add(variant);
}

function showEmptyMessage(message) {
  consoleEl.innerHTML = `<div class="console-empty">${escapeHtml(message)}<span class="cursor">_</span></div>`;
}

async function runParser(event) {
  event.preventDefault();
  const text = textarea.value.trim();

  consoleEl.innerHTML = "";

  if (!text) {
    showEmptyMessage("No instructions to parse");
    return;
  }

  setStatus("RUNNING", "tag-running");
  runBtn.disabled = true;

  let steps = [];
  try {
    const response = await fetch("/parse", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ instruction: text }),
    });

    if (!response.ok) throw new Error("Bad response");

    const data = await response.json();
    steps = data.steps || [];
  } catch (err) {
    consoleEl.innerHTML = `<div class="console-line"><span class="line-badge badge-error">COULD NOT REACH PARSER</span></div>`;
    setStatus("ERROR");
    runBtn.disabled = false;
    return;
  }

  if (steps.length === 0) {
    showEmptyMessage("No recognizable steps found");
    setStatus("IDLE");
    runBtn.disabled = false;
    return;
  }

  for (let i = 0; i < steps.length; i++) {
    await new Promise((resolve) => setTimeout(resolve, STEP_DELAY_MS));
    const step = steps[i];

    const line = document.createElement("div");
    line.className = "console-line";
    line.innerHTML = `
      <span class="line-time">[${formatTime((i + 1) * STEP_DELAY_MS)}]</span>
      <span class="line-badge ${BADGE_CLASS[step.type] || "badge-unknown"}">${escapeHtml(step.label)}</span>
      ${step.detail ? `<span class="line-detail">${escapeHtml(step.detail)}</span>` : ""}
    `;
    consoleEl.appendChild(line);
    consoleEl.scrollTop = consoleEl.scrollHeight;
  }

  setStatus(`DONE · ${steps.length} STEP${steps.length > 1 ? "S" : ""}`, "tag-done");
  runBtn.disabled = false;
}

textarea.addEventListener("input", updateGutter);
textarea.addEventListener("scroll", () => {
  gutter.scrollTop = textarea.scrollTop;
});
form.addEventListener("submit", runParser);

updateGutter();
