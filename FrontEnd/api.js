// api.js
// Capa de acceso a datos con tolerancia a fallos.
// Si el backend no responde, devolvemos un mock local sin romper el front.

(() => {
  const API_BASE = "/fresh-bowl-api"; // Ajusta si tu backend está en otro path

  async function safeFetch(url, options = {}) {
    try {
      const res = await fetch(url, {
        headers: { "Content-Type": "application/json" },
        ...options,
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      console.warn("safeFetch fallback ->", err?.message || err);
      return null; // Señal de fallo para que el front use mock/localStorage
    }
  }

  // --- Productos ---
  async function getProductos() {
    const data = await safeFetch(`${API_BASE}/productos`);
    if (data && Array.isArray(data)) return data;

    // Fallback: mock mínimo si el backend está caído
    return [
      {
        id: "ens-01",
        nombre: "César Clásica",
        precio: 4990,
        imagen:
          "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800",
      },
      {
        id: "ens-02",
        nombre: "Quinoa Power",
        precio: 5490,
        imagen:
          "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=800",
      },
      {
        id: "ens-03",
        nombre: "Fresca Mediterránea",
        precio: 5990,
        imagen:
          "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800",
      },
    ];
  }

  // --- Carrito (persistido localmente) ---
  function readCart() {
    try {
      const raw = localStorage.getItem("fb_cart");
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  }

  function writeCart(items) {
    localStorage.setItem("fb_cart", JSON.stringify(items));
    return items;
  }

  // API pública en window
  window.API = {
    getProductos,
    readCart,
    writeCart,
  };
})();
