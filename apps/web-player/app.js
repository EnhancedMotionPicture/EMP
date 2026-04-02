const videoEl = document.getElementById("video");
const empFileEl = document.getElementById("empFile");
const videoFileEl = document.getElementById("videoFile");
const tracksEl = document.getElementById("tracks");
const logEl = document.getElementById("log");
const offsetEl = document.getElementById("offset");

let empData = null;
let firedKeys = new Set();

videoFileEl.addEventListener("change", () => {
  const file = videoFileEl.files[0];
  if (!file) return;
  videoEl.src = URL.createObjectURL(file);
});

empFileEl.addEventListener("change", async () => {
  const file = empFileEl.files[0];
  if (!file) return;
  const text = await file.text();
  empData = JSON.parse(text);
  firedKeys = new Set();
  renderTracks();
  logEl.textContent = "EMP file loaded. Press play.";
});

function renderTracks() {
  if (!empData) {
    tracksEl.textContent = "No file loaded.";
    return;
  }
  const lines = [];
  lines.push(`Title: ${empData.project?.title || ""}`);
  lines.push(`Media: ${empData.media?.src || ""}`);
  lines.push("");
  for (const track of empData.tracks || []) {
    lines.push(`${track.id} [${track.type}] -> ${track.target}`);
    for (const ev of track.events || []) {
      lines.push(`  ${ev.t_ms}ms ${ev.shape} intensity=${ev.intensity} dur=${ev.dur_ms}`);
    }
    lines.push("");
  }
  tracksEl.textContent = lines.join("\n");
}

videoEl.addEventListener("timeupdate", () => {
  if (!empData) return;
  const offset = Number(offsetEl.value || 0);
  const ms = Math.floor(videoEl.currentTime * 1000) + offset;
  const logs = [];
  for (const track of empData.tracks || []) {
    for (let i = 0; i < (track.events || []).length; i++) {
      const ev = track.events[i];
      const key = `${track.id}-${i}`;
      if (!firedKeys.has(key) && ms >= ev.t_ms) {
        firedKeys.add(key);
        logs.push(`${ms}ms -> ${track.type} ${track.target} ${ev.shape} intensity=${ev.intensity}`);
      }
    }
  }
  if (logs.length) {
    logEl.textContent = logs.join("\n") + "\n" + logEl.textContent;
  }
});

videoEl.addEventListener("seeked", () => {
  firedKeys = new Set();
  logEl.textContent = "Seek detected. Event state reset.";
});
