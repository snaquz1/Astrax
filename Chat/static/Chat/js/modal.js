const modalwin = document.getElementById("modal")

function openModal() {
  modalwin.style.display = "block";
}

function closeModal() {
  modalwin.style.display = "none";
}

const invitelink = document.getElementById("invitelink")

invitelink.innerText = `http://${location.host}/invite/` + invitelink.innerText;
//copy link

const copyLinkBtn = document.querySelector(".copy-link-btn");

copyLinkBtn.addEventListener("click", function (){
  const link = invitelink.innerText;
  navigator.clipboard.writeText(link);
  copyLinkBtn.textContent = "Скопировано"
  setTimeout(function (){
    copyLinkBtn.textContent = "Копировать"
  }, 1200)
})








