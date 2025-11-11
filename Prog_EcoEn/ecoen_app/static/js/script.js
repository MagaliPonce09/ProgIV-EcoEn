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

// === MODO OSCURO/CLARO ===
document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("themeToggle");
  const body = document.body;

  if (!toggleBtn) return;

  if (localStorage.getItem("theme") === "dark") {
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
});

// === CARRITO DE COMPRAS ===
document.addEventListener("DOMContentLoaded", () => {
  const carritoLista = document.getElementById("carrito-lista");
  const carritoTotal = document.getElementById("carrito-total");
  const monedaSelect = document.getElementById("moneda");

  let carrito = [];
  let tasaCambio = {
    USD: 1,
    EUR: 0.92,
    ARS: 880,
  };

  function actualizarCarrito() {
    carritoLista.innerHTML = "";
    let totalUSD = 0;

    carrito.forEach((item, index) => {
      totalUSD += item.precio;

      const li = document.createElement("li");
      li.className =
        "list-group-item d-flex justify-content-between align-items-center";
      li.innerHTML = `
        <span>${item.nombre}</span>
        <span>$${item.precio}</span>
        <button onclick="eliminarDelCarrito(${index})" class="btn btn-sm btn-danger">🗑️</button>
      `;
      carritoLista.appendChild(li);
    });

    const moneda = monedaSelect.value;
    const totalConvertido = totalUSD * tasaCambio[moneda];
    carritoTotal.textContent = totalConvertido.toFixed(2) + " " + moneda;
  }

  window.eliminarDelCarrito = function (index) {
    carrito.splice(index, 1);
    actualizarCarrito();
  };

  document.querySelectorAll(".add-to-cart").forEach((btn) => {
    btn.addEventListener("click", () => {
      const nombre = btn.getAttribute("data-product");
      const precio = parseFloat(btn.getAttribute("data-price"));
      carrito.push({ nombre, precio });
      actualizarCarrito();
    });
  });

  monedaSelect?.addEventListener("change", actualizarCarrito);
});

// === MENÚ LATERAL ===
function toggleMenu() {
  const menu = document.getElementById("menu-lateral");
  const toggle = document.getElementById("menu-toggle");

  menu.classList.toggle("active");
  toggle.classList.toggle("active");
}