// static/js/chatbot.js

// =========================
// Referencias a elementos
// =========================

document.addEventListener("DOMContentLoaded", () => {
const btn = document.getElementById("chatbot-button");
const win = document.getElementById("chatbot-window");
const closeBtn = document.getElementById("chatbot-close");
const messages = document.getElementById("chatbot-messages");
const input = document.getElementById("chatbot-input");
const sendBtn = document.getElementById("chatbot-send");
const quickReplies = document.getElementById("chatbot-quick-replies");

// =========================
/* Apertura / cierre con slide-in */
// =========================
chatbotButton.addEventListener("click", () => {
    chatbotWindow.classList.remove("hidden");
  });

  // Cerrar chatbot
  chatbotClose.addEventListener("click", () => {
    chatbotWindow.classList.add("hidden");
  });

// =========================
/* Utilidades de mensajes */
// =========================
function addMessage(sender, text) {
  const div = document.createElement("div");
  div.className = `message ${sender === "Tú" ? "user" : "bot"}`;
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

// =========================
/* Envío de texto libre */
// =========================
function sendFreeText() {
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  addMessage("Tú", text);
  postToBot(text);
}

sendBtn?.addEventListener("click", sendFreeText);
input?.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendFreeText();
});

// =========================
/* Post al backend */
// =========================
function postToBot(text) {
  fetch("/chatbot-response/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  })
    .then((res) => res.json())
    .then((data) => {
      // respuesta principal del bot
      addMessage("EcoBot", data.reply);

      // opciones dinámicas (categorías, productos, confirmaciones, tips…)
      if (data.options && Array.isArray(data.options)) {
        renderQuickOptions(data.options);
      }
    })
    .catch(() => addMessage("EcoBot", "Lo siento, hubo un problema al procesar tu mensaje."));
}

// =========================
/* Botones rápidos iniciales */
// =========================
quickReplies?.addEventListener("click", (e) => {
  const target = e.target;
  if (target.tagName !== "BUTTON") return;

  const action = target.getAttribute("data-action");
  switch (action) {
    case "asistencia":
      sendQuickReply("Asistencia técnica");
      break;
    case "recomendacion":
      sendQuickReply("Recomendación de productos");
      break;
    case "compra":
      sendQuickReply("Realizar compra");
      break;
    case "tips":
      sendQuickReply("Tips de sostenibilidad");
      break;
  }
});

// =========================
/* Enviar texto desde botón */
// =========================
function sendQuickReply(text) {
  addMessage("Tú", text);
  postToBot(text);
}

// =========================
/* Render de opciones dinámicas */
// =========================
function renderQuickOptions(options) {
  // Limpia y renderiza nuevas opciones contextuales
  quickReplies.innerHTML = "";
  options.forEach(opt => {
    const b = document.createElement("button");
    b.textContent = opt.label;
    b.addEventListener("click", () => {
      addMessage("Tú", opt.send);
      postToBot(opt.send);
    });
    quickReplies.appendChild(b);
  });
}

// =========================
/* Mensaje de bienvenida */
// =========================
window.addEventListener("DOMContentLoaded", () => {
  addMessage("EcoBot", "Hola 👋 Soy EcoBot. ¿En que puedo ayudarte hoy?
  ¿Buscas asistencia técnica, recomendaciones, comprar, o tips de sostenibilidad?");
  }
});


