attachBtn = document.getElementById("attach-btn");
inputFiles = document.getElementById("input-files");

attachBtn.addEventListener("click", function () {
    if(inputFiles.style.display === "none"){
        inputFiles.style.display = "flex"
    }else {
        inputFiles.style.display = "none"
    }

})

const box = document.getElementById("messages");
if (box) {
    box.scrollTop = box.scrollHeight;
}
