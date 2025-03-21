document.addEventListener("DOMContentLoaded", function () {
  const selectElement = document.getElementById("president-select");
  const presidentImage = document.getElementById("president-image");

  selectElement.addEventListener("change", function () {
    const selectedValue = selectElement.value;
    let newImageSrc = "";

    if (selectedValue === "lincoln") {
      newImageSrc = "/assets/abraham_lincoln_headshot.png";
    } else if (selectedValue === "jefferson") {
      newImageSrc = "/assets/thomas_jefferson_headshot.png";
    }

    presidentImage.src = newImageSrc;
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
