function openModal() {
  document.getElementById("modal").style.display = "block";
}

function closeModal() {
  document.getElementById("modal").style.display = "none";
}

const invitelink = document.getElementById("invitelink")

invitelink.innerText = `http://${location.host}/invite/` + invitelink.innerText;

