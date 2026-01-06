const messagesDiv = document.getElementById("messages");
const sendBtn = document.getElementById("send-btn");
const input = document.getElementById("user-input");
const fileInput = document.getElementById("file-input");

let pendingImageFile = null;   // store without auto-sending
let pendingImagePreview = null;

function appendMessage(text, role, imageURL=null) {
  const div = document.createElement("div");
  div.className = `message ${role}`;

  if (imageURL) {
    const img = document.createElement("img");
    img.src = imageURL;
    img.style.maxWidth = "200px";
    img.style.display = "block";
    img.style.marginBottom = "8px";
    div.appendChild(img);
  }

  if (text) div.appendChild(document.createTextNode(text));
  messagesDiv.appendChild(div);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function showPendingImagePreview(file) {
  const url = URL.createObjectURL(file);

  // Remove previous preview if exists
  if (pendingImagePreview) pendingImagePreview.remove();

  // Insert preview above input box
  pendingImagePreview = document.createElement("img");
  pendingImagePreview.src = url;
  pendingImagePreview.style.maxWidth = "150px";
  pendingImagePreview.style.margin = "10px 0";
  pendingImagePreview.style.borderRadius = "6px";

  input.parentElement.insertBefore(pendingImagePreview, input);
}

async function sendMessage() {
  const text = input.value.trim();
  const file = pendingImageFile;

  if (!text && !file) return;

  // show the user message
  let imageURL = file ? URL.createObjectURL(file) : null;
  appendMessage(text, "user", imageURL);

  // build request
  const form = new FormData();
  form.append("text", text || "");
  if (file) form.append("image", file);

  // clear UI state
  input.value = "";
  pendingImageFile = null;

  if (pendingImagePreview) {
    pendingImagePreview.remove();
    pendingImagePreview = null;
  }

  fileInput.value = "";

  // send to backend
  const response = await fetch("http://localhost:8000/chat", {
    method: "POST",
    body: form,
  });

  const data = await response.json();
  appendMessage(data.reply, "assistant");
}

// user clicks send
sendBtn.onclick = sendMessage;

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// drag-and-drop image
document.addEventListener("dragover", (e) => e.preventDefault());
document.addEventListener("drop", (e) => {
  e.preventDefault();
  if (e.dataTransfer.files.length) {
    const file = e.dataTransfer.files[0];
    pendingImageFile = file;
    showPendingImagePreview(file);
  }
});

// selecting image (no auto-send)
fileInput.onchange = () => {
  const file = fileInput.files[0];
  if (!file) return;

  pendingImageFile = file;
  showPendingImagePreview(file);
};
