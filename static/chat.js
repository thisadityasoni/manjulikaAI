const msgerChat = document.querySelector(".msger-chat");
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");

chatForm.addEventListener("submit", event => {
  event.preventDefault();

  const msgText = userInput.value.trim();
  if (!msgText) return;

  appendMessage("You", "right", msgText);
  userInput.value = "";

  fetch(chatForm.action, {
    method: 'POST',
    body: new URLSearchParams(new FormData(chatForm))
  })
  .then(response => response.text())
  .then(data => {
    appendMessage("Manjulika", "left", data);
  })
  .catch(error => console.error('Error:', error));
});

function appendMessage(name, side, text) {
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>
        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop = msgerChat.scrollHeight;
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}
