document.getElementById("chatbot-button").onclick = function() {
  const chatWindow = document.getElementById("chatbot-window");
  chatWindow.style.display = chatWindow.style.display === "none" ? "block" : "none";
};

async function sendMessage() {
  const message = document.getElementById("userMessage").value;
  const response = await fetch("/chat/", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message})
  });
  const data = await response.json();

  const chatLog = document.getElementById("chatbot-messages");
  chatLog.innerHTML += `<p><b>Tú:</b> ${message}</p>`;
  chatLog.innerHTML += `<p style="color:#4CAF50"><b>EcoBot:</b> ${data.reply}</p>`;
  document.getElementById("userMessage").value = "";
}
