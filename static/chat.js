const msgerChat = document.querySelector(".msger-chat");
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");

// Attach event listener to the chat form
chatForm.addEventListener("submit", event => {
  event.preventDefault(); // Prevent form submission

  const msgText = userInput.value.trim();
  if (!msgText) return; // If no message, return

  appendMessage("You", "right", msgText); // Append user's message to chat window
  userInput.value = ""; // Clear the input field

  // Send message to the server
  sendMessage(msgText);
});

// Function to append a message to the chat window
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

  msgerChat.insertAdjacentHTML("beforeend", msgHTML); // Append message HTML to chat window
  msgerChat.scrollTop = msgerChat.scrollHeight; // Scroll to bottom of chat window
}

// Function to format date as HH:MM
function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();
  return `${h.slice(-2)}:${m.slice(-2)}`;
}

// Function to send message to the server
function sendMessage(message) {
  fetch(chatForm.action, {
    method: 'POST',
    body: new URLSearchParams({ user_input: message }) // Send user input as form data
  })
  .then(response => response.text())
  .then(data => {
    appendMessage("Manjulika", "left", data); // Append server response to chat window
  })
  .catch(error => console.error('Error:', error));
}
