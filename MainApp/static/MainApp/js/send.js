document.addEventListener('click', async (e) => {

  if (!e.target.classList.contains('copy-btn')) return;

  const msg = e.target.closest('.message');
  const text = msg.querySelector('.msg-text').innerText;

  try {
    await navigator.clipboard.writeText(text);

    e.target.textContent = "✔";
    setTimeout(() => e.target.textContent = "📋", 1200);

  } catch {
    e.target.textContent = "✖";
    setTimeout(() => e.target.textContent = "📋", 1200);
  }
});

const textarea = document.getElementById("text");
const form = textarea.closest("form");

let sending = false;

// Enter => submit (Shift+Enter = newline)
textarea.addEventListener("keydown", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    if (sending) return;         // 🔒 блок дубля
    sending = true;
    htmx.trigger(form, "submit");
  }
});

// Когда HTMX запрос закончился — разблокируем
document.body.addEventListener("htmx:afterRequest", function (e) {
  if (e.detail.elt === form) {
    sending = false;
  }
});

// Если запрос упал — тоже разблокируем
document.body.addEventListener("htmx:responseError", function (e) {
  if (e.detail.elt === form) {
    sending = false;
  }
});

// Перед запросом решаем: автоскроллить или нет
document.body.addEventListener("htmx:beforeRequest", function (e) {
  const box = document.getElementById("messages");
  if (!box) return;

  const triggerEl = e.detail.elt; // кто инициировал запрос (form или poller)

  // Если это отправка с формы — всегда скроллим вниз
  if (triggerEl && triggerEl.tagName === "FORM") {
    shouldAutoScroll = true;
    return;
  }

  // Если это poller — скроллим только если пользователь уже был внизу
  if (triggerEl && triggerEl.id === "poller") {
    shouldAutoScroll = isNearBottom(box);
  }
});

// После вставки новых сообщений скроллим ТОЛЬКО если можно
document.body.addEventListener("htmx:afterSwap", function (e) {
  if (!e.detail.target || e.detail.target.id !== "messages") return;
  if (!shouldAutoScroll) return;

  const box = document.getElementById("messages");
  if (!box) return;

  requestAnimationFrame(() => {
    box.scrollTop = box.scrollHeight;
  });
});