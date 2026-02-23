document.body.addEventListener('htmx:afterRequest', function (e) {
// нас интересует только poller
if (!e.target || e.target.id !== 'poller') return;

const xhr = e.detail.xhr;
if (!xhr) return;

// если ответ непустой — пришли новые сообщения
if (xhr.responseText && xhr.responseText.trim().length > 0) {
  const a = document.getElementById('msg-sound');
  if (a) a.play().catch(() => {});
}
});
