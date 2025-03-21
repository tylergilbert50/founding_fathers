document.addEventListener("DOMContentLoaded", function () {
  const selectElement = document.getElementById("president-select");
  const presidentImage = document.getElementById("president-image");
  const presidentName = document.getElementById("selected-president");
  const userInput = document.getElementById("user-input");

  selectElement.addEventListener("change", function () {
    const selected = selectElement.value;

    const presidentData = {
      lincoln: {
        name: "Abraham Lincoln",
        image: "/assets/abraham_lincoln_headshot.png",
      },
      jefferson: {
        name: "Thomas Jefferson",
        image: "/assets/thomas_jefferson_headshot.png",
      },
    };

    const data = presidentData[selected];
    presidentImage.src = data.image;
    presidentName.textContent = data.name;
  });

  // Listen for Enter key in the input field
  userInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      event.preventDefault(); // Prevent form submission behavior
      sendMessage();
    }
  });
});

function sendMessage() {
  const userInput = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");

  if (userInput.value.trim() === "") return;

  const userMessage = `<div><strong>You:</strong> ${userInput.value}</div>`;
  chatBox.innerHTML += userMessage;

  fetch("/chat", {
    method: "POST",
    body: JSON.stringify({ message: userInput.value }),
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((data) => {
      const botMessage = `<div><strong>AI:</strong> ${data.response}</div>`;
      chatBox.innerHTML += botMessage;
      chatBox.scrollTop = chatBox.scrollHeight;
    });

  userInput.value = "";
}
