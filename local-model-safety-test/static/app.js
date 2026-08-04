let sessionId = null;

const baselineLog = document.getElementById("baseline-log");
const injectedLog = document.getElementById("injected-log");
const messageInput = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const templateSelect = document.getElementById("template-select");
const sessionList = document.getElementById("session-list");
const newSessionBtn = document.getElementById("new-session-btn");
const targetSelect = document.getElementById("target-select");

function appendMessage(log, role, content) {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  const roleLabel = document.createElement("div");
  roleLabel.className = "role";
  roleLabel.textContent = role;
  const body = document.createElement("div");
  body.textContent = content;
  div.appendChild(roleLabel);
  div.appendChild(body);
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
  return div;
}

function appendLoader(log) {
  const div = document.createElement("div");
  div.className = "msg assistant loader";
  div.innerHTML = '<div class="role">assistant</div><div class="dots"><span></span><span></span><span></span></div>';
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
  return div;
}

async function startSession() {
  const res = await fetch("/api/session/new", { method: "POST" });
  const data = await res.json();
  sessionId = data.session_id;
  baselineLog.innerHTML = "";
  injectedLog.innerHTML = "";
  await loadSessionList();
}

function formatDate(isoString) {
  const d = new Date(isoString);
  return d.toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

async function loadSessionList() {
  const res = await fetch("/api/sessions");
  const items = await res.json();

  sessionList.innerHTML = "";
  for (const item of items) {
    const li = document.createElement("li");
    li.dataset.sessionId = item.id;
    if (item.id === sessionId) li.classList.add("active");

    const dateSpan = document.createElement("span");
    dateSpan.className = "session-date";
    dateSpan.textContent = formatDate(item.created_at);

    const snippetSpan = document.createElement("span");
    snippetSpan.textContent = item.first_message
      ? item.first_message.slice(0, 50)
      : "(empty session)";

    li.appendChild(dateSpan);
    li.appendChild(snippetSpan);
    li.addEventListener("click", () => openSession(item.id));
    sessionList.appendChild(li);
  }
}

async function openSession(id) {
  const res = await fetch(`/api/sessions/${id}`);
  const data = await res.json();

  sessionId = id;
  baselineLog.innerHTML = "";
  injectedLog.innerHTML = "";

  for (const msg of data.baseline) {
    appendMessage(baselineLog, msg.role, msg.content);
  }
  for (const msg of data.injected) {
    appendMessage(injectedLog, msg.role, msg.content);
  }

  document.querySelectorAll("#session-list li").forEach((li) => {
    li.classList.toggle("active", Number(li.dataset.sessionId) === id);
  });
}

async function sendMessage() {
  const message = messageInput.value.trim();
  if (!message || !sessionId) return;

  sendBtn.disabled = true;
  messageInput.value = "";

  const target = targetSelect.value;
  const sendBaseline = target === "both" || target === "baseline";
  const sendInjected = target === "both" || target === "injected";

  let injectedUserDiv = null;
  let baselineLoader = null;
  let injectedLoader = null;

  if (sendBaseline) {
    appendMessage(baselineLog, "user", message);
    baselineLoader = appendLoader(baselineLog);
  }
  if (sendInjected) {
    injectedUserDiv = appendMessage(injectedLog, "user", message);
    injectedLoader = appendLoader(injectedLog);
  }

  const templateId = templateSelect.value;

  try {
    const res = await fetch("/api/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message, template_id: templateId, target }),
    });
    const data = await res.json();

    if (sendBaseline) {
      baselineLoader.remove();
      appendMessage(baselineLog, "assistant", data.baseline_reply);
    }
    if (sendInjected) {
      injectedLoader.remove();
      injectedUserDiv.lastElementChild.textContent = data.injected_message;
      appendMessage(injectedLog, "assistant", data.injected_reply);
    }

    await loadSessionList();
  } catch (err) {
    if (baselineLoader) baselineLoader.remove();
    if (injectedLoader) injectedLoader.remove();
    appendMessage(sendBaseline ? baselineLog : injectedLog, "assistant", `Error: ${err}`);
  } finally {
    sendBtn.disabled = false;
  }
}

sendBtn.addEventListener("click", sendMessage);
messageInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});
newSessionBtn.addEventListener("click", startSession);

startSession();
