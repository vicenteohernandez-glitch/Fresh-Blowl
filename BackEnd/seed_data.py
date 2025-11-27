"""
Script para poblar la base de datos con datos de prueba.
Ejecutar: python seed_data.py
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext

# Conexión a MongoDB
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "freshbowl"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Datos de prueba
CATEGORIAS = [
    {"nombre": "Ensaladas Clásicas", "descripcion": "Las favoritas de siempre", "activa": True},
    {"nombre": "Bowls Proteicos", "descripcion": "Alto contenido en proteínas", "activa": True},
    {"nombre": "Veganas", "descripcion": "100% plant-based", "activa": True},
    {"nombre": "Bebidas", "descripcion": "Jugos y aguas frescas", "activa": True},
]

PRODUCTOS = [
    {
        "nombre": "Ensalada César",
        "descripcion": "Clásica ensalada con lechuga romana, pollo grillado, queso parmesano, crutones crujientes y aderezo César casero.",
        "precio": 8990,
        "imagen_url": "https://images.unsplash.com/photo-1546793665-c74683f339c1?w=800",
        "categoria_nombre": "Ensaladas Clásicas",
        "disponible": True,
        "stock": 50,
        "ingredientes": ["Lechuga romana", "Pollo", "Parmesano", "Crutones", "Aderezo César"]
    },
    {
        "nombre": "Quinoa Power Bowl",
        "descripcion": "Bowl energético con quinoa, espinaca fresca, palta, tomates cherry, garbanzos y vinagreta de limón.",
        "precio": 9490,
        "imagen_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800",
        "categoria_nombre": "Bowls Proteicos",
        "disponible": True,
        "stock": 30,
        "ingredientes": ["Quinoa", "Espinaca", "Palta", "Tomate cherry", "Garbanzos"]
    },
    {
        "nombre": "Mediterránea",
        "descripcion": "Mezcla de verdes con aceitunas kalamata, queso feta, pepino, cebolla morada y vinagreta mediterránea.",
        "precio": 8490,
        "imagen_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800",
        "categoria_nombre": "Ensaladas Clásicas",
        "disponible": True,
        "stock": 40,
        "ingredientes": ["Mix verdes", "Aceitunas", "Queso feta", "Pepino", "Cebolla morada"]
    },
    {
        "nombre": "Buddha Bowl Vegano",
        "descripcion": "Bowl colorido con arroz integral, tofu marinado, edamame, zanahoria, repollo morado y salsa de maní.",
        "precio": 9990,
        "imagen_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800",
        "categoria_nombre": "Veganas",
        "disponible": True,
        "stock": 25,
        "ingredientes": ["Arroz integral", "Tofu", "Edamame", "Zanahoria", "Repollo"]
    },
    {
        "nombre": "Pollo Teriyaki Bowl",
        "descripcion": "Bowl japonés con arroz, pollo teriyaki, edamame, pepino, zanahoria y semillas de sésamo.",
        "precio": 10490,
        "imagen_url": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=800",
        "categoria_nombre": "Bowls Proteicos",
        "disponible": True,
        "stock": 35,
        "ingredientes": ["Arroz", "Pollo teriyaki", "Edamame", "Pepino", "Sésamo"]
    },
    {
        "nombre": "Salmón & Aguacate",
        "descripcion": "Ensalada premium con salmón ahumado, palta, mix de verdes, alcaparras y aderezo de eneldo.",
        "precio": 12990,
        "imagen_url": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=800",
        "categoria_nombre": "Bowls Proteicos",
        "disponible": True,
        "stock": 20,
        "ingredientes": ["Salmón ahumado", "Palta", "Mix verdes", "Alcaparras", "Aderezo eneldo"]
    },
    {
        "nombre": "Detox Verde",
        "descripcion": "Ensalada detox con kale, espinaca, pepino, apio, manzana verde y aderezo de jengibre.",
        "precio": 7990,
        "imagen_url": "https://images.unsplash.com/photo-1607532941433-304659e8198a?w=800",
        "categoria_nombre": "Veganas",
        "disponible": True,
        "stock": 45,
        "ingredientes": ["Kale", "Espinaca", "Pepino", "Apio", "Manzana verde"]
    },
    {
        "nombre": "Limonada de Menta",
        "descripcion": "Refrescante limonada natural con hojas de menta fresca.",
        "precio": 2990,
        "imagen_url": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=800",
        "categoria_nombre": "Bebidas",
        "disponible": True,
        "stock": 100,
        "ingredientes": ["Limón", "Menta", "Azúcar"]
    },
]

USUARIOS = [
    {
        "nombre": "Admin Fresh Bowl",
        "email": "admin@freshbowl.cl",
        "hash_password": pwd_context.hash("admin123"),
        "telefono": "+56912345678",
        "email_verificado": True,
        "activo": True
    },
    {
        "nombre": "Cliente Demo",
        "email": "cliente@demo.cl",
        "hash_password": pwd_context.hash("demo123"),
        "telefono": "+56987654321",
        "email_verificado": True,
        "activo": True
    }
]

async def seed_database():
    print("🌱 Conectando a MongoDB...")
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Limpiar colecciones existentes (opcional)
    print("🗑️  Limpiando datos anteriores...")
    await db.categorias.delete_many({})
    await db.productos.delete_many({})
    await db.usuarios.delete_many({})
    
    # Insertar categorías
    print("📁 Insertando categorías...")
    cat_result = await db.categorias.insert_many(CATEGORIAS)
    cat_ids = {cat["nombre"]: str(id) for cat, id in zip(CATEGORIAS, cat_result.inserted_ids)}
    print(f"   ✅ {len(cat_result.inserted_ids)} categorías creadas")
    
    # Insertar productos con referencia a categorías
    print("🥗 Insertando productos...")
    for prod in PRODUCTOS:
        cat_nombre = prod.pop("categoria_nombre", None)
        if cat_nombre and cat_nombre in cat_ids:
            prod["categoria_id"] = cat_ids[cat_nombre]
    
    prod_result = await db.productos.insert_many(PRODUCTOS)
    print(f"   ✅ {len(prod_result.inserted_ids)} productos creados")
    
    # Insertar usuarios
    print("👤 Insertando usuarios...")
    user_result = await db.usuarios.insert_many(USUARIOS)
    print(f"   ✅ {len(user_result.inserted_ids)} usuarios creados")
    
    # Mostrar resumen
    print("\n" + "="*50)
    print("🎉 BASE DE DATOS POBLADA EXITOSAMENTE")
    print("="*50)
    print("\n📊 Resumen:")
    print(f"   • Categorías: {await db.categorias.count_documents({})}")
    print(f"   • Productos: {await db.productos.count_documents({})}")
    print(f"   • Usuarios: {await db.usuarios.count_documents({})}")
    print("\n🔑 Credenciales de prueba:")
    print("   • Admin: admin@freshbowl.cl / admin123")
    print("   • Cliente: cliente@demo.cl / demo123")
    print("\n🌐 Endpoints para probar:")
    print("   • http://localhost:8000/api/productos/")
    print("   • http://localhost:8000/api/categorias/")
    print("   • http://localhost:8000/docs (Swagger UI)")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
