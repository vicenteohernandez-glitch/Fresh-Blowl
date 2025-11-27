from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Database:
    client: Optional[AsyncIOMotorClient] = None
    database = None
    
db = Database()

# Configuración de MongoDB
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "freshbowl")

async def get_database():
    return db.database

async def connect_to_mongo():
    """Conectar a MongoDB"""
    db.client = AsyncIOMotorClient(MONGODB_URL)
    db.database = db.client[DATABASE_NAME]
    print(f"✅ Conectado a MongoDB: {DATABASE_NAME}")

async def close_mongo_connection():
    """Cerrar conexión a MongoDB"""
    if db.client is not None:
        db.client.close()
        db.client = None
        db.database = None
        print("❌ Desconectado de MongoDB")

def get_collection(collection_name: str):
    """Obtener una colección de MongoDB"""
    if db.database is None:
        raise Exception("No hay conexión a MongoDB. Asegúrate de ejecutar connect_to_mongo primero.")
    return db.database[collection_name]
