from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from models.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse, UsuarioLogin
from database import get_collection
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def serialize_doc(doc):
    """Convierte ObjectId a string para serialización JSON"""
    if doc is None:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

def serialize_docs(docs):
    """Serializa una lista de documentos"""
    return [serialize_doc(doc) for doc in docs]

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_usuario(usuario: UsuarioCreate):
    """Crear un nuevo usuario"""
    collection = get_collection("usuarios")
    
    # Verificar si el email ya existe
    existing_user = await collection.find_one({"email": usuario.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    usuario_dict = usuario.model_dump(exclude={"password"})
    usuario_dict["hash_password"] = get_password_hash(usuario.password)
    
    result = await collection.insert_one(usuario_dict)
    created_usuario = await collection.find_one({"_id": result.inserted_id})
    
    return serialize_doc(created_usuario)

@router.get("/")
async def get_usuarios(skip: int = 0, limit: int = 100):
    """Obtener lista de usuarios"""
    collection = get_collection("usuarios")
    usuarios = await collection.find().skip(skip).limit(limit).to_list(length=limit)
    return serialize_docs(usuarios)

@router.get("/{usuario_id}")
async def get_usuario(usuario_id: str):
    """Obtener un usuario por ID"""
    collection = get_collection("usuarios")
    
    if not ObjectId.is_valid(usuario_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    usuario = await collection.find_one({"_id": ObjectId(usuario_id)})
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    return serialize_doc(usuario)

@router.put("/{usuario_id}")
async def update_usuario(usuario_id: str, usuario: UsuarioUpdate):
    """Actualizar un usuario"""
    collection = get_collection("usuarios")
    
    if not ObjectId.is_valid(usuario_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    update_data = {k: v for k, v in usuario.model_dump(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay datos para actualizar")
    
    result = await collection.update_one(
        {"_id": ObjectId(usuario_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    updated_usuario = await collection.find_one({"_id": ObjectId(usuario_id)})
    return serialize_doc(updated_usuario)

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: str):
    """Eliminar un usuario"""
    collection = get_collection("usuarios")
    
    if not ObjectId.is_valid(usuario_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.delete_one({"_id": ObjectId(usuario_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    return None

@router.post("/login")
async def login(credentials: UsuarioLogin):
    """Autenticar usuario"""
    collection = get_collection("usuarios")
    
    usuario = await collection.find_one({"email": credentials.email})
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    if not verify_password(credentials.password, usuario["hash_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    if not usuario.get("activo", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    # Devolver datos del usuario (sin password)
    return {
        "_id": str(usuario["_id"]),
        "nombre": usuario.get("nombre", ""),
        "email": usuario["email"],
        "telefono": usuario.get("telefono", ""),
        "email_verificado": usuario.get("email_verificado", False),
        "activo": usuario.get("activo", True)
    }
