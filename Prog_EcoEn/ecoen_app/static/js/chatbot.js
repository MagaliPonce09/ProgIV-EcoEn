
document.addEventListener("DOMContentLoaded", function() {
    const button = document.getElementById("chatbot-button");
    const windowEl = document.getElementById("chatbot-window");
    const closeBtn = document.getElementById("chatbot-close");
    const input = document.getElementById("chatbot-input");
    const sendBtn = document.getElementById("chatbot-send");
    const quickReplies = document.querySelectorAll("#chatbot-quick-replies button");

    // 🔊 Sonidos UI personalizados (usando rutas absolutas a /static/)
    const soundBubble = new Audio("/static/sounds/bubble.mp3");
    const soundMagic  = new Audio("/static/sounds/magic.mp3");
    const soundRetro  = new Audio("/static/sounds/retro.mp3");
    soundBubble.volume = 0.6;
    soundMagic.volume  = 0.6;
    soundRetro.volume  = 0.6;

    // Abrir ventana desde el ícono EcoBot
    button.addEventListener("click", () => {
        windowEl.style.display = "flex";   // mostrar
        windowEl.classList.add("show");
        windowEl.setAttribute("aria-hidden", false);
    });

    // Cerrar con la "X"
    closeBtn.addEventListener("click", () => {
        windowEl.classList.remove("show");
        windowEl.setAttribute("aria-hidden", true);
        setTimeout(() => { windowEl.style.display = "none"; }, 400); // espera animación y oculta
    });

    // Cerrar al hacer click fuera de la ventana
    document.addEventListener("click", (e) => {
        if (windowEl.classList.contains("show")) {
            const isClickInside = windowEl.contains(e.target) || button.contains(e.target);
            if (!isClickInside) {
                windowEl.classList.remove("show");
                windowEl.setAttribute("aria-hidden", true);
                setTimeout(() => { windowEl.style.display = "none"; }, 400);
            }
        }
    });

    // Función auxiliar para añadir mensajes
    function appendMsg(text, who = "bot") {
        const body = document.getElementById("chatbot-messages");
        const div = document.createElement("div");
        div.className = who === "user" ? "user-msg msg" : "bot-msg msg";

        const span = document.createElement("span");

        if (who === "bot") {
            // Bot: agrega el emoji 🌱 antes del texto
            span.textContent = `🌱 ${text}`;
        } else {
            // Usuario: solo texto, sin avatar ni emoji
            span.textContent = text;
        }

        div.appendChild(span);
        body.appendChild(div);
        body.scrollTop = body.scrollHeight;
    }

    // 🔧 Tips ecológicos aleatorios
    const tips = [
        "🌱 Usa bolsas reutilizables en lugar de plásticas.",
        "💡 Apaga las luces cuando no las necesites.",
        "🚲 Opta por la bicicleta para trayectos cortos.",
        "♻️ Separa residuos reciclables en tu hogar.",
        "🌍 Reduce el consumo de agua cerrando la canilla al cepillarte."
    ];
    function obtenerTipEcologico() {
        const randomIndex = Math.floor(Math.random() * tips.length);
        return tips[randomIndex];
    }

    // 🔧 Función de respuesta con includes
    function replyFor(msg) {
        const t = msg.toLowerCase();

        if (t.includes("energía") || t.includes("energia")) {
            return "💡 Tip: Cambia a LED, usa regletas con interruptor y programa horarios de uso.";
        }
        if (t.includes("asistencia") || t.includes("soporte")) {
            return "🔧 Asistencia: Contacta soporte@EcoEn.com o describe tu problema.";
        }
        if (t.includes("horario")) {
            return "🕘 Horarios: Atendemos de lunes a viernes de 9 a 18 hs.";
        }
        if (t.includes("envio") || t.includes("envíos")) {
            return "📦 Envíos: Realizamos envíos a todo el país en 3 a 5 días hábiles.";
        }
        if (t.includes("precio") || t.includes("precios")) {
            return "💲 El precio depende del catálogo, consulta nuestra tienda online.";
        }
        if (t.includes("gracias")) {
            return "🤝 ¡De nada! Siempre a tu servicio.";
        }
        if (t.includes("compra")) {
            return "🛒 Puedes explorar productos en la sección 'Productos'.";
        }
        if (t.includes("tips")) {
            return "📘 Recuerda separar residuos y ahorrar agua.";
        }

        // Si no coincide con nada, devuelve tip ecológico aleatorio
        return obtenerTipEcologico();
    }

    // Enviar mensaje con indicador de escritura
    function sendMessage() {
        const msg = input.value.trim();
        if (!msg) return;

        appendMsg(`👤 ${msg}`, "user");
        input.value = "";

        // Mostrar indicador de escritura
        const body = document.getElementById("chatbot-messages");
        const typingDiv = document.createElement("div");
        typingDiv.className = "typing-indicator";
        typingDiv.innerHTML = "<span>.</span><span>.</span><span>.</span>";
        body.appendChild(typingDiv);
        body.scrollTop = body.scrollHeight;

        setTimeout(() => {
            typingDiv.remove();
            const response = replyFor(msg);
            appendMsg(response, "bot");
        }, 1200);
    }

    // Botón enviar
    sendBtn.addEventListener("click", sendMessage);

    // Enviar con Enter
    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    });

    // Botones rápidos con sonidos
    quickReplies.forEach(btn => {
        btn.addEventListener("click", () => {
            input.value = btn.dataset.action;

            // Selección de sonido según el botón
            const action = btn.dataset.action.toLowerCase();
            let s = soundBubble; // default

            if (action.includes("asistencia")) s = soundMagic;
            else if (action.includes("energía") || action.includes("energia")) s = soundBubble;
            else if (action.includes("horarios")) s = soundRetro;
            else if (action.includes("envíos") || action.includes("envio")) s = soundMagic;
            else if (action.includes("precios")) s = soundRetro;

            s.currentTime = 0;
            s.play().catch(() => {});

            sendMessage();
        });
    });

    // Mensaje de bienvenida inicial
    appendMsg("Hola, soy EcoBot. ¿En qué puedo ayudarte hoy?", "bot");
});
