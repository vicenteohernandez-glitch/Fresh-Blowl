from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import connect_to_mongo, close_mongo_connection
from routers import (
    usuarios,
    roles,
    productos,
    categorias,
    ingredientes,
    pedidos,
    carritos,
    cupones,
    direcciones,
    notificaciones,
    pagos,
    envios,
    comprobantes
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: conectar a MongoDB
    await connect_to_mongo()
    yield
    # Shutdown: cerrar conexión
    await close_mongo_connection()

app = FastAPI(
    title="Fresh Bowl API",
    description="API para sistema de venta de ensaladas personalizadas",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(roles.router, prefix="/api/roles", tags=["Roles"])
app.include_router(productos.router, prefix="/api/productos", tags=["Productos"])
app.include_router(categorias.router, prefix="/api/categorias", tags=["Categorías"])
app.include_router(ingredientes.router, prefix="/api/ingredientes", tags=["Ingredientes"])
app.include_router(pedidos.router, prefix="/api/pedidos", tags=["Pedidos"])
app.include_router(carritos.router, prefix="/api/carritos", tags=["Carritos"])
app.include_router(cupones.router, prefix="/api/cupones", tags=["Cupones"])
app.include_router(direcciones.router, prefix="/api/direcciones", tags=["Direcciones"])
app.include_router(notificaciones.router, prefix="/api/notificaciones", tags=["Notificaciones"])
app.include_router(pagos.router, prefix="/api/pagos", tags=["Pagos"])
app.include_router(envios.router, prefix="/api/envios", tags=["Envíos"])
app.include_router(comprobantes.router, prefix="/api/comprobantes", tags=["Comprobantes"])

@app.get("/")
async def root():
    return {
        "message": "ViChoPremium API - Sistema de venta de ensaladas personalizadas",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
