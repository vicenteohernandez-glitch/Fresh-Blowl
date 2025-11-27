# 🥗 Fresh Bowl - Sistema de Pedidos de Ensaladas

Sistema web completo para gestión de pedidos de ensaladas y bowls saludables.

## 📋 Requisitos Previos

### Software necesario:
- **Python 3.10+** (probado con 3.13)
- **MongoDB** corriendo en `localhost:27017`
- **Navegador web moderno** (Chrome, Firefox, Edge)

### Verificar instalación:
```powershell
python --version    # Python 3.10+
mongod --version    # MongoDB instalado
```

---

## 🚀 Instalación y Ejecución

### 1. Instalar dependencias del Backend

```powershell
cd Fresh-Blowl/BackEnd
pip install -r requirements.txt
```

### 2. Iniciar MongoDB

Asegúrate de que MongoDB esté corriendo:
```powershell
# Windows - si tienes MongoDB como servicio
net start MongoDB

# O inicia mongod manualmente
mongod --dbpath "C:\data\db"
```

### 3. Iniciar el Servidor Backend

```powershell
cd Fresh-Blowl/BackEnd
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Deberías ver:
```
✅ Conectado a MongoDB: freshbowl
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 4. Abrir el Frontend

Abre en tu navegador:
```
Fresh-Blowl/FrontEnd/index.html
```

O usa Live Server en VS Code para mejor experiencia.

---

## 📁 Estructura del Proyecto

```
Fresh-Blowl/
├── BackEnd/
│   ├── main.py              # Punto de entrada FastAPI
│   ├── database.py          # Conexión MongoDB
│   ├── requirements.txt     # Dependencias Python
│   ├── models/              # Modelos Pydantic
│   │   ├── usuario.py
│   │   ├── producto.py
│   │   ├── pedido.py
│   │   ├── ingrediente.py
│   │   └── ...
│   └── routers/             # Endpoints API
│       ├── usuarios.py
│       ├── productos.py
│       ├── pedidos.py
│       ├── ingredientes.py
│       └── ...
│
└── FrontEnd/
    ├── index.html           # Página principal
    ├── api.js               # Capa de acceso a API
    ├── estilos.css          # Estilos globales
    ├── B1_registro.html     # Registro de usuarios
    ├── B4_Inicio_Sesion.html # Login
    ├── B6_ListaProducto.html # Catálogo
    └── ...                  # 26 páginas HTML total
```

---

## 🔌 API Endpoints

Base URL: `http://127.0.0.1:8000/api`

| Recurso | Endpoints |
|---------|-----------|
| Usuarios | `POST /usuarios/`, `POST /usuarios/login`, `GET /usuarios/{id}`, `PUT /usuarios/{id}` |
| Productos | `GET /productos/`, `GET /productos/{id}` |
| Categorías | `GET /categorias/`, `GET /categorias/{id}` |
| Ingredientes | `GET /ingredientes/`, `GET /ingredientes/alertas`, `PUT /ingredientes/{id}` |
| Pedidos | `POST /pedidos/`, `GET /pedidos/`, `GET /pedidos/{id}`, `PUT /pedidos/{id}` |
| Pagos | `POST /pagos/`, `PUT /pagos/{id}/aprobar` |
| Notificaciones | `GET /notificaciones/?usuario_id={id}` |

Documentación interactiva: `http://127.0.0.1:8000/docs`

---

## 👤 Usuarios de Prueba

| Email | Contraseña | Rol |
|-------|------------|-----|
| admin@freshbowl.cl | admin123 | Admin |
| cliente@demo.cl | demo123 | Cliente |

---

## 📱 Páginas del Sistema

### Autenticación
- `B1_registro.html` - Registro de nuevos usuarios
- `B3_Recuperar_Contraseña.html` - Recuperar contraseña
- `B4_Inicio_Sesion.html` - Inicio de sesión

### Catálogo
- `B6_ListaProducto.html` - Lista de productos
- `B8_Detalle_Producto.html` - Detalle de producto
- `B15_seleccion_ingredientes.html` - Personalizar ingredientes

### Pedidos
- `B18_Crear_Pedido.html` - Crear nuevo pedido
- `B19_Modificar_Cancelar.html` - Modificar/cancelar pedido
- `B11_Historial_Pedidos.html` - Historial de pedidos
- `B23_confirmacion_tiempo_real.html` - Estado del pedido

### Pagos
- `B21_pasarela_pago.html` - Pasarela de pago
- `B20_Confirmacion_Pago.html` - Confirmación de pago
- `B22_boleta_digital.html` - Boleta digital

### Envíos
- `B24_seleccion_entrega.html` - Selección de entrega
- `B25_seguimiento_pedido.html` - Seguimiento de pedido

### Perfil
- `B33_ver_perfil.html` - Ver perfil
- `B34_Editar_Perfil.html` - Editar perfil
- `B35_Cambio_Contrasena.html` - Cambiar contraseña
- `B36_Preferencias.html` - Preferencias
- `B37_Eliminar_Cuenta.html` - Eliminar cuenta

### Administración
- `B27_disponibilidad_ingredientes.html` - Gestión de ingredientes
- `B28_actualizacion_stock.html` - Actualizar stock
- `B29_Alertas_Agotamiento.html` - Alertas de stock

### Otros
- `B13_Top_Ensaladas.html` - Estadísticas de ventas
- `B26_notificaciones_cliente.html` - Notificaciones

---

## 🧪 Probar la API

```powershell
# Obtener productos
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/productos/" -Method GET

# Obtener ingredientes
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/ingredientes/" -Method GET

# Obtener alertas de stock
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/ingredientes/alertas" -Method GET

# Registrar usuario
$body = '{"nombre":"Test","email":"test@test.cl","password":"test123"}'
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/usuarios/" -Method POST -Body $body -ContentType "application/json"
```

---

## 🔧 Solución de Problemas

### Error: "No connection could be made"
- Verifica que el servidor backend esté corriendo en puerto 8000
- Verifica que MongoDB esté corriendo

### Error: "Could not import module main"
- Asegúrate de ejecutar desde la carpeta `BackEnd/`

### CORS Error en navegador
- El backend ya tiene CORS configurado para localhost
- Usa `http://127.0.0.1:8000` en lugar de `localhost:8000`

---

## 📊 Base de Datos

MongoDB automáticamente crea la base de datos `freshbowl` con las colecciones:
- `usuarios`
- `productos`
- `categorias`
- `ingredientes`
- `pedidos`
- `pagos`
- `envios`
- `notificaciones`

---

## 🎨 Tecnologías

**Backend:**
- FastAPI (Python)
- Motor (MongoDB async driver)
- Pydantic v2

**Frontend:**
- HTML5 / CSS3
- JavaScript (Vanilla)
- Chart.js (gráficos)

---

## 📝 Licencia

Proyecto académico - Fresh Bowl © 2025
