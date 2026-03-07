const messages = document.getElementById("messages");
const input = document.getElementById("text");
const sendBtn = document.getElementById("send-btn");
const close = document.getElementById("close");
const statusLogs = document.getElementById("status-logs");

messages.scrollTop = messages.scrollHeight;

function addLine(text) {
  const div = document.createElement("div");
  div.className = "message incoming"
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

function addStatusLog(log){
  const div = document.createElement("div");
  div.textContent = log;
  statusLogs.appendChild(div);
  statusLogs.scrollTop = messages.scrollHeight;
}

// ws или wss (если сайт на https)
const scheme = (location.protocol === "https:") ? "wss" : "ws";

// создаём соединение
const socket = new WebSocket(`${scheme}://${location.host}/ws/chat/${chat_id}/`);

socket.onopen = () => addStatusLog("Подключено по WebSocket ✅");
socket.onclose = () => addStatusLog("Соединение WebSocket закрыто ❌");
socket.onerror = () => addStatusLog("Произошла ошибка ❌");

// сервер прислал сообщение
socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  addLine(`${data.message}`);
};

// отправка
sendBtn.onclick = () => {
  const text = input.value.trim();
  if (!text) return;
  socket.send(JSON.stringify({ message: text }));
  input.value = "";
  input.focus();
};


input.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    sendBtn.click();
  }
});