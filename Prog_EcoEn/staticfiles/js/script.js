console.log("✅ script.js cargado correctamente");

// === SLIDER ===
document.querySelectorAll(".slider").forEach((slider) => {
  const slides = slider.querySelectorAll(".slide");
  const dots = slider.querySelectorAll(".dot");
  const nextBtn = slider.querySelector("#next");
  const prevBtn = slider.querySelector("#prev");
  let current = 0;

  function showSlide(index) {
    slides.forEach((slide, i) => {
      slide.classList.toggle("active", i === index);
      if (dots[i]) dots[i].classList.toggle("active", i === index);
    });
    current = index;
  }

  nextBtn?.addEventListener("click", () => {
    showSlide((current + 1) % slides.length);
  });

  prevBtn?.addEventListener("click", () => {
    showSlide((current - 1 + slides.length) % slides.length);
  });

  dots.forEach((dot, i) => {
    dot.addEventListener("click", () => showSlide(i));
  });

  setInterval(() => {
    showSlide((current + 1) % slides.length);
  }, 5000);
});

// === MODO OSCURO/CLARO, CARRITO, PAGO, PUNTUACIÓN ===
document.addEventListener("DOMContentLoaded", () => {
  // === MODO OSCURO/CLARO ===
  const toggleBtn = document.getElementById("themeToggle");
  const body = document.body;

  if (toggleBtn) {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
      body.classList.add("dark-mode");
      body.classList.remove("light-mode");
      toggleBtn.textContent = "☀️ Modo claro";
    } else {
      body.classList.add("light-mode");
      body.classList.remove("dark-mode");
      toggleBtn.textContent = "🌙 Modo oscuro";
    }

    toggleBtn.addEventListener("click", () => {
      body.classList.toggle("dark-mode");
      body.classList.toggle("light-mode");

      if (body.classList.contains("dark-mode")) {
        toggleBtn.textContent = "☀️ Modo claro";
        localStorage.setItem("theme", "dark");
      } else {
        toggleBtn.textContent = "🌙 Modo oscuro";
        localStorage.setItem("theme", "light");
      }
    });
  }

  // === CARRITO DE COMPRAS ===
  const carritoLista = document.getElementById("carrito-lista");
  const carritoTotal = document.getElementById("carrito-total");
  const monedaSelect = document.getElementById("moneda");

  let carrito = [];
  const tasaCambio = { USD: 1, EUR: 0.92, ARS: 880 };

  function actualizarCarrito() {
    carritoLista.innerHTML = "";
    let totalUSD = 0;

    carrito.forEach((item, index) => {
      totalUSD += item.precio;
      const li = document.createElement("li");
      li.className =
        "list-group-item d-flex justify-content-between align-items-center";

      const spanNombre = document.createElement("span");
      spanNombre.textContent = item.nombre;

      const spanPrecio = document.createElement("span");
      spanPrecio.textContent = `$${item.precio}`;

      const btnEliminar = document.createElement("button");
      btnEliminar.className = "btn btn-sm btn-danger";
      btnEliminar.textContent = "🗑️";
      btnEliminar.addEventListener("click", () => {
        carrito.splice(index, 1);
        actualizarCarrito();
      });

      li.append(spanNombre, spanPrecio, btnEliminar);
      carritoLista.appendChild(li);
    });

    const moneda = monedaSelect?.value || "ARS";
    const totalConvertido = totalUSD * tasaCambio[moneda];
    carritoTotal.textContent = totalConvertido.toFixed(2) + " " + moneda;
  }

  document.querySelectorAll(".add-to-cart").forEach((btn) => {
    btn.addEventListener("click", () => {
      const nombre = btn.dataset.product;
      const precio = parseFloat(btn.dataset.price);
      carrito.push({ nombre, precio });
      actualizarCarrito();
    });
  });

  monedaSelect?.addEventListener("change", actualizarCarrito);

  // === MÉTODOS DE PAGO ===
  const btnComprar = document.getElementById("btn-comprar");
  const metodosPago = document.getElementById("metodos-pago");
  const datosTransferencia = document.getElementById("datos-transferencia");

  btnComprar?.addEventListener("click", () => {
    if (carritoLista.children.length === 0) {
      alert("Tu carrito está vacío.");
      return;
    }
    metodosPago.classList.remove("d-none");
  });

  document.getElementById("btn-mercado-pago")?.addEventListener("click", () => {
    window.location.href = "/confirmar-pago/mercado_pago/";
  });

  document.getElementById("btn-transferencia")?.addEventListener("click", () => {
    datosTransferencia.classList.remove("d-none");
  });

  // === PUNTUACIÓN DE PRODUCTOS ===
  document.querySelectorAll(".rating").forEach((ratingBlock) => {
    const stars = ratingBlock.querySelectorAll(".star");
    const productName = ratingBlock
      .closest(".card-body")
      ?.querySelector(".card-title")?.textContent;

    const savedRating = localStorage.getItem(`rating_${productName}`);
    if (savedRating) {
      stars.forEach((s, i) => {
        s.classList.toggle("text-warning", i < parseInt(savedRating));
      });
    }

    stars.forEach((star) => {
      star.addEventListener("click", () => {
        const selectedValue = parseInt(star.dataset.value);
        stars.forEach((s, i) => {
          s.classList.remove("text-warning");
          if (i < selectedValue) s.classList.add("text-warning");
        });

        if (productName) {
          localStorage.setItem(`rating_${productName}`, selectedValue);
          alert(
            `Puntuaste "${productName}" con ${selectedValue} estrella${
              selectedValue > 1 ? "s" : ""
            } ⭐`
          );
        }
      });
    });
  });
});

// === MENÚ LATERAL ===
function toggleMenu() {
  const menu = document.getElementById("menu-lateral");
  const icon = document.getElementById("menu-icon");

  menu.classList.toggle("active");

  icon.textContent = menu.classList.contains("active")
    ? "✖"
    : icon.dataset.default || "☰";
}
