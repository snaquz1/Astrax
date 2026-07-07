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
  try {
    const data = JSON.parse(event.data);
    console.log("👉 Вот что РЕАЛЬНО прилетело с сервера:", data);

    // ВАРИАНТ А: Сервер прислал готовый HTML (для сообщений с файлами)
    if (data.html) {
      console.log("Тип: Готовый HTML с бэкенда");
      const tempDiv = document.createElement("div");
      tempDiv.innerHTML = data.html.trim();
      const messageElement = tempDiv.firstElementChild;

      if (messageElement) {
        messages.appendChild(messageElement);
        messages.scrollTop = messages.scrollHeight;
        return; // Всё сделали, выходим
      }
    }

    // ВАРИАНТ Б: Сервер прислал просто текст (обычное сообщение по WebSocket)
    // Проверяем все возможные ключи, где может лежать текст
    const text = data.message || data.text || data.content;
    const username = data.username || data.sender;

    if (text) {
      console.log("Тип: Сырой текст. Рисуем через addMessage()");
      addMessage(text, username);
      return;
    }

    console.warn("💀 Сервер прислал какой-то странный формат, я не понял что с ним делать:", data);

  } catch (error) {
    console.error("💥 Ошибка при разборе сообщения:", error);
  }
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


