let sessionId = null;

const baselineLog = document.getElementById("baseline-log");
const injectedLog = document.getElementById("injected-log");
const messageInput = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const templateSelect = document.getElementById("template-select");

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
}

async function sendMessage() {
  const message = messageInput.value.trim();
  if (!message || !sessionId) return;

  sendBtn.disabled = true;
  messageInput.value = "";

  appendMessage(baselineLog, "user", message);
  const injectedUserDiv = appendMessage(injectedLog, "user", message);

  const baselineLoader = appendLoader(baselineLog);
  const injectedLoader = appendLoader(injectedLog);

  const templateId = templateSelect.value;

  try {
    const res = await fetch("/api/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message, template_id: templateId }),
    });
    const data = await res.json();

    baselineLoader.remove();
    injectedLoader.remove();

    injectedUserDiv.lastElementChild.textContent = data.injected_message;

    appendMessage(baselineLog, "assistant", data.baseline_reply);
    appendMessage(injectedLog, "assistant", data.injected_reply);
  } catch (err) {
    baselineLoader.remove();
    injectedLoader.remove();
    appendMessage(baselineLog, "assistant", `Error: ${err}`);
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

startSession();
