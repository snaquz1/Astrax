const messages = document.getElementById("messages");
const input = document.getElementById("text");
const sendBtn = document.getElementById("send-btn");
const close = document.getElementById("close");
const statusLogs = document.getElementById("status-logs");
const fileInput = document.getElementById("input-files");

messages.scrollTop = messages.scrollHeight;

function addMessage(text, username) {
  const div = document.createElement("div");
  console.log(username, user)
  if (username === user){
    div.className = "message outgoing"
  }else {
    div.className = "message incoming"
  }
    div.innerHTML = `
    <div class="sender-username">${username}:</div>
  <div class="msg-text">${text}</div>
<button class="copy-btn">📋</button>
  `;

  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

function addStatusLog(log){
  const div = document.createElement("div");
  div.textContent = log;
  statusLogs.appendChild(div);
  statusLogs.scrollTop = messages.scrollHeight;
}

const scheme = (location.protocol === "https:") ? "wss" : "ws";

// создаём соединение
function connect(){
  statusLogs.innerHTML = "";
  const socket = new WebSocket(`${scheme}://${location.host}/ws/chat/${chat_id}/`);

  socket.onopen = () => addStatusLog("Подключено по WebSocket ✅");
  socket.onclose = () => {
    addStatusLog("Соединение WebSocket закрыто ❌");
    addStatusLog("Пробуем подключиться...")
    setTimeout(connect, 2000)
  };
  socket.onerror = () => addStatusLog("Произошла ошибка ❌");

// сервер прислал сообщение
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    // Создаем временный контейнер, чтобы превратить строку в HTML
    const tempDiv = document.createElement("div");
    tempDiv.innerHTML = data.html;

    // Берем готовое сообщение из твоего шаблона message.html
    const messageElement = tempDiv.firstElementChild;

    // Добавляем в окно чата
    messages.appendChild(messageElement);

    // Скроллим вниз
    messages.scrollTop = messages.scrollHeight;
  };


  sendBtn.onclick = async () => {
  const text = input.value.trim();
  const files = fileInput ? fileInput.files : [];
  if (!text && files.length === 0) return;

  if (files.length > 0) {
    const formData = new FormData();
    formData.append('text', text);
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i]);
    }

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    await fetch(`/chat/${chat_id}/send`, {
      method: 'POST',
      body: formData,
      headers: {'X-CSRFToken': csrfToken}
    });

    input.value = "";
    if (fileInput) fileInput.value = "";
    input.focus();
  }else {
    socket.send(JSON.stringify({ message: text }));
      input.value = "";
      input.focus();}
  }
}

connect();

input.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    sendBtn.click();
  }
});


