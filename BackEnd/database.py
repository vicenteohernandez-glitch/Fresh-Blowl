from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

class Database:
    client: Optional[AsyncIOMotorClient] = None
    
db = Database()

async def get_database():
    return db.client

async def connect_to_mongo():
    """Conectar a MongoDB"""
    # Configurar según tus necesidades
    MONGODB_URL = "mongodb://localhost:27017"
    DATABASE_NAME = "vichopremium"
    
    db.client = AsyncIOMotorClient(MONGODB_URL)[DATABASE_NAME]
    print("✅ Conectado a MongoDB")

async def close_mongo_connection():
    """Cerrar conexión a MongoDB"""
    if db.client:
        db.client = None
        print("❌ Desconectado de MongoDB")

def get_collection(collection_name: str):
    """Obtener una colección de MongoDB"""
    return db.client[collection_name]
