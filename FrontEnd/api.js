// api.js
// Capa de acceso a datos con tolerancia a fallos.
// Si el backend no responde, devolvemos un mock local sin romper el front.

(() => {
  // URL del backend FastAPI - cambiar en producción
  const API_BASE = "http://localhost:8000/api";

  // ============= UTILIDADES =============
  
  // Obtener token de sesión
  function getToken() {
    const user = JSON.parse(localStorage.getItem("usuarioFB") || "{}");
    return user.token || null;
  }

  // Headers con autenticación
  function getHeaders() {
    const headers = { "Content-Type": "application/json" };
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
    return headers;
  }

  // Fetch seguro con manejo de errores
  async function safeFetch(url, options = {}) {
    try {
      const res = await fetch(url, {
        headers: getHeaders(),
        ...options,
      });
      
      if (!res.ok) {
        const error = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
        throw new Error(error.detail || `HTTP ${res.status}`);
      }
      
      // Para respuestas 204 No Content
      if (res.status === 204) return { success: true };
      
      return await res.json();
    } catch (err) {
      console.warn("API Error:", err?.message || err);
      return null;
    }
  }

  // ============= USUARIOS =============
  
  async function registrarUsuario(nombre, email, password, telefono = null) {
    const data = await safeFetch(`${API_BASE}/usuarios/`, {
      method: "POST",
      body: JSON.stringify({ nombre, email, password, telefono }),
    });
    return data;
  }

  async function loginUsuario(email, password) {
    const data = await safeFetch(`${API_BASE}/usuarios/login`, {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    
    if (data && data._id) {
      // Guardar usuario en localStorage
      localStorage.setItem("usuarioFB", JSON.stringify({
        _id: data._id,
        nombre: data.nombre,
        email: data.email,
        telefono: data.telefono || "",
        token: data.token || null
      }));
    }
    return data;
  }

  async function getUsuario(usuarioId) {
    return await safeFetch(`${API_BASE}/usuarios/${usuarioId}`);
  }

  async function updateUsuario(usuarioId, datos) {
    return await safeFetch(`${API_BASE}/usuarios/${usuarioId}`, {
      method: "PUT",
      body: JSON.stringify(datos),
    });
  }

  async function deleteUsuario(usuarioId) {
    return await safeFetch(`${API_BASE}/usuarios/${usuarioId}`, {
      method: "DELETE",
    });
  }

  function getUsuarioActual() {
    try {
      return JSON.parse(localStorage.getItem("usuarioFB") || "null");
    } catch {
      return null;
    }
  }

  function logout() {
    localStorage.removeItem("usuarioFB");
  }

  function isLoggedIn() {
    return getUsuarioActual() !== null;
  }

  // ============= PRODUCTOS =============
  
  async function getProductos(categoriaId = null, activo = null) {
    let url = `${API_BASE}/productos/`;
    const params = [];
    if (categoriaId) params.push(`categoria_id=${categoriaId}`);
    if (activo !== null) params.push(`activo=${activo}`);
    if (params.length) url += '?' + params.join('&');
    
    const data = await safeFetch(url);
    if (data && Array.isArray(data)) return data;

    // Fallback: mock mínimo si el backend está caído
    return [
      {
        _id: "ens-01",
        nombre: "César Clásica",
        precio: 4990,
        descripcion: "Lechuga romana, pollo, parmesano y crutones",
        imagen_url: "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800",
      },
      {
        _id: "ens-02",
        nombre: "Quinoa Power",
        precio: 5490,
        descripcion: "Quinoa, espinaca, palta y tomate cherry",
        imagen_url: "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=800",
      },
      {
        _id: "ens-03",
        nombre: "Mediterránea",
        precio: 5990,
        descripcion: "Mix verdes, aceitunas, queso feta y pepino",
        imagen_url: "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800",
      },
    ];
  }

  async function getProducto(productoId) {
    return await safeFetch(`${API_BASE}/productos/${productoId}`);
  }

  // ============= CATEGORÍAS =============
  
  async function getCategorias() {
    const data = await safeFetch(`${API_BASE}/categorias/`);
    if (data && Array.isArray(data)) return data;
    
    // Fallback mock
    return [
      { _id: "cat-01", nombre: "Ensaladas Clásicas" },
      { _id: "cat-02", nombre: "Bowls Proteicos" },
      { _id: "cat-03", nombre: "Veganas" },
    ];
  }

  async function getCategoria(categoriaId) {
    return await safeFetch(`${API_BASE}/categorias/${categoriaId}`);
  }

  // ============= INGREDIENTES =============
  
  async function getIngredientes(adicional = null) {
    let url = `${API_BASE}/ingredientes/`;
    if (adicional !== null) url += `?adicional=${adicional}`;
    return await safeFetch(url);
  }

  // ============= CARRITO (Local + Sync con Backend) =============
  
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

  function clearCart() {
    localStorage.removeItem("fb_cart");
    return [];
  }

  function addToCart(producto, cantidad = 1) {
    const cart = readCart();
    const idx = cart.findIndex(x => x.id === producto._id || x.id === producto.id);
    
    if (idx >= 0) {
      cart[idx].qty += cantidad;
    } else {
      cart.push({
        id: producto._id || producto.id,
        nombre: producto.nombre,
        precio: producto.precio_base || producto.precio,
        imagen: producto.imagen || "",
        qty: cantidad
      });
    }
    
    return writeCart(cart);
  }

  function removeFromCart(productoId) {
    const cart = readCart().filter(x => x.id !== productoId);
    return writeCart(cart);
  }

  function getCartTotal() {
    return readCart().reduce((acc, item) => acc + (item.precio * item.qty), 0);
  }

  // ============= PEDIDOS =============
  
  async function crearPedido(pedidoData) {
    return await safeFetch(`${API_BASE}/pedidos/`, {
      method: "POST",
      body: JSON.stringify(pedidoData),
    });
  }

  async function getPedidos(usuarioId = null, estado = null) {
    let url = `${API_BASE}/pedidos/`;
    const params = [];
    if (usuarioId) params.push(`usuario_id=${usuarioId}`);
    if (estado) params.push(`estado=${estado}`);
    if (params.length) url += `?${params.join("&")}`;
    
    return await safeFetch(url);
  }

  async function getPedido(pedidoId) {
    return await safeFetch(`${API_BASE}/pedidos/${pedidoId}`);
  }

  async function getHistorialPedidos(usuarioId) {
    return await safeFetch(`${API_BASE}/pedidos/usuario/${usuarioId}/historial`);
  }

  async function updatePedido(pedidoId, datos) {
    return await safeFetch(`${API_BASE}/pedidos/${pedidoId}`, {
      method: "PUT",
      body: JSON.stringify(datos),
    });
  }

  // Alias para compatibilidad
  async function actualizarPedido(pedidoId, datos) {
    return updatePedido(pedidoId, datos);
  }

  async function cancelarPedido(pedidoId) {
    return await safeFetch(`${API_BASE}/pedidos/${pedidoId}`, {
      method: "DELETE",
    });
  }

  // ============= PAGOS =============
  
  async function crearPago(pagoData) {
    return await safeFetch(`${API_BASE}/pagos/`, {
      method: "POST",
      body: JSON.stringify(pagoData),
    });
  }

  async function aprobarPago(pagoId) {
    return await safeFetch(`${API_BASE}/pagos/${pagoId}/aprobar`, {
      method: "POST",
    });
  }

  // ============= ENVÍOS =============
  
  async function getEnvio(envioId) {
    return await safeFetch(`${API_BASE}/envios/${envioId}`);
  }

  async function getEnvioByTracking(tracking) {
    return await safeFetch(`${API_BASE}/envios/tracking/${tracking}`);
  }

  // ============= NOTIFICACIONES =============
  
  async function getNotificaciones(usuarioId) {
    return await safeFetch(`${API_BASE}/notificaciones/?usuario_id=${usuarioId}`);
  }

  // ============= API PÚBLICA =============
  
  window.API = {
    // Auth
    registrarUsuario,
    loginUsuario,
    getUsuario,
    updateUsuario,
    actualizarUsuario: updateUsuario,
    deleteUsuario,
    getUsuarioActual,
    logout,
    isLoggedIn,
    
    // Productos
    getProductos,
    getProducto,
    getIngredientes,
    
    // Categorías
    getCategorias,
    getCategoria,
    
    // Carrito (local)
    readCart,
    writeCart,
    clearCart,
    addToCart,
    removeFromCart,
    getCartTotal,
    
    // Pedidos
    crearPedido,
    getPedidos,
    getPedido,
    getHistorialPedidos,
    updatePedido,
    actualizarPedido,
    cancelarPedido,
    
    // Pagos
    crearPago,
    aprobarPago,
    
    // Envíos
    getEnvio,
    getEnvioByTracking,
    
    // Notificaciones
    getNotificaciones,
  };

  console.log("✅ API Fresh Bowl cargada correctamente");
})();
