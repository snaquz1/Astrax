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

