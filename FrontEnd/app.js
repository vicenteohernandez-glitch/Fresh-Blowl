// app.js
// Render de productos + carrito con estado en localStorage.
// No truena si el backend falla (usa mock de api.js automáticamente).

(() => {
  // ---- Selectores base (ajusta IDs/clases si tu HTML difiere) ----
  const $grid = document.querySelector("#productos-grid");
  const $badge = document.querySelector("#cart-count");
  const $panel = document.querySelector("#cart-panel");
  const $toggle = document.querySelector("#cart-toggle");
  const $list = document.querySelector("#cart-list");
  const $total = document.querySelector("#cart-total");
  const CURRENCY = "CLP";

  // Guardrails si falta algún nodo
  function qfail(selector) {
    throw new Error(`Falta en el DOM: ${selector}`);
  }
  $grid || qfail("#productos-grid");
  $badge || qfail("#cart-count");
  $panel || qfail("#cart-panel");
  $toggle || qfail("#cart-toggle");
  $list || qfail("#cart-list");
  $total || qfail("#cart-total");

  // ---- Estado ----
  let cart = API.readCart(); // [{id, nombre, precio, qty, imagen}]

  // ---- Utilidades ----
  const fmt = (n) =>
    new Intl.NumberFormat("es-CL", {
      style: "currency",
      currency: CURRENCY,
      maximumFractionDigits: 0,
    }).format(n);

  function saveCart() {
    cart = API.writeCart(cart);
    renderCart();
  }

  function cartCount() {
    return cart.reduce((acc, it) => acc + it.qty, 0);
  }

  function cartTotal() {
    return cart.reduce((acc, it) => acc + it.qty * it.precio, 0);
  }

  function addToCart(product) {
    const idx = cart.findIndex((x) => x.id === product.id);
    if (idx >= 0) cart[idx].qty += 1;
    else cart.push({ ...product, qty: 1 });
    saveCart();
  }

  function decFromCart(id) {
    const idx = cart.findIndex((x) => x.id === id);
    if (idx < 0) return;
    cart[idx].qty -= 1;
    if (cart[idx].qty <= 0) cart.splice(idx, 1);
    saveCart();
  }

  function removeFromCart(id) {
    cart = cart.filter((x) => x.id !== id);
    saveCart();
  }

  // ---- Render de Productos ----
  function productCard(p) {
    return `
      <article class="product-card">
        <div class="img-wrap">
          <img src="${p.imagen}" alt="${p.nombre}" loading="lazy">
        </div>
        <div class="info">
          <h3>${p.nombre}</h3>
          <p class="price">${fmt(p.precio)}</p>
          <button class="btn-add" data-id="${p.id}">Agregar</button>
        </div>
      </article>
    `;
  }

  async function renderProducts() {
    const productos = await API.getProductos();
    $grid.innerHTML = productos.map(productCard).join("");

    // Delegación de eventos: agregar al carrito
    $grid.addEventListener("click", (ev) => {
      const btn = ev.target.closest(".btn-add");
      if (!btn) return;
      const id = btn.dataset.id;
      const p = productos.find((x) => x.id === id);
      if (!p) return;
      addToCart(p);
      // feedback rápido
      btn.disabled = true;
      const old = btn.textContent;
      btn.textContent = "✓ Agregado";
      setTimeout(() => {
        btn.disabled = false;
        btn.textContent = old;
      }, 600);
    });
  }

  // ---- Render de Carrito ----
  function renderCart() {
    // Badge
    $badge.textContent = cartCount();

    // Lista
    if (cart.length === 0) {
      $list.innerHTML = `<li class="empty">Tu carrito está vacío</li>`;
    } else {
      $list.innerHTML = cart
        .map(
          (it) => `
        <li class="cart-item">
          <img src="${it.imagen}" alt="${it.nombre}">
          <div class="meta">
            <strong>${it.nombre}</strong>
            <span>${fmt(it.precio)} c/u</span>
            <div class="qty">
              <button class="qty-dec" data-id="${it.id}">−</button>
              <span>${it.qty}</span>
              <button class="qty-inc" data-id="${it.id}">+</button>
            </div>
          </div>
          <div class="right">
            <span class="line">${fmt(it.qty * it.precio)}</span>
            <button class="remove" title="Quitar" data-id="${it.id}">×</button>
          </div>
        </li>`
        )
        .join("");
    }

    // Total
    $total.textContent = fmt(cartTotal());
  }

  // Delegación dentro del panel del carrito
  $panel.addEventListener("click", (ev) => {
    const inc = ev.target.closest(".qty-inc");
    const dec = ev.target.closest(".qty-dec");
    const del = ev.target.closest(".remove");
    if (inc) {
      const id = inc.dataset.id;
      const item = cart.find((x) => x.id === id);
      if (item) {
        item.qty += 1;
        saveCart();
      }
    } else if (dec) {
      decFromCart(dec.dataset.id);
    } else if (del) {
      removeFromCart(del.dataset.id);
    }
  });

  // Toggle del carrito
  $toggle.addEventListener("click", () => {
    $panel.classList.toggle("open");
  });

  // Cierra carrito al hacer click fuera (opcional)
  document.addEventListener("click", (e) => {
    const isPanel = e.target.closest("#cart-panel");
    const isToggle = e.target.closest("#cart-toggle");
    if (!isPanel && !isToggle) $panel.classList.remove("open");
  });

  // Init
  renderProducts().then(renderCart);
})();
