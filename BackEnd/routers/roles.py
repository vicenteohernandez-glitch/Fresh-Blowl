from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from models.rol import RolCreate, RolUpdate, RolResponse, UsuarioRol
from database import get_collection

router = APIRouter()

@router.post("/", response_model=RolResponse, status_code=status.HTTP_201_CREATED)
async def create_rol(rol: RolCreate):
    """Crear un nuevo rol"""
    collection = get_collection("roles")
    
    rol_dict = rol.dict()
    result = await collection.insert_one(rol_dict)
    created_rol = await collection.find_one({"_id": result.inserted_id})
    
    return created_rol

@router.get("/", response_model=List[RolResponse])
async def get_roles(skip: int = 0, limit: int = 100):
    """Obtener lista de roles"""
    collection = get_collection("roles")
    roles = await collection.find().skip(skip).limit(limit).to_list(length=limit)
    return roles

@router.get("/{rol_id}", response_model=RolResponse)
async def get_rol(rol_id: str):
    """Obtener un rol por ID"""
    collection = get_collection("roles")
    
    if not ObjectId.is_valid(rol_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    rol = await collection.find_one({"_id": ObjectId(rol_id)})
    if not rol:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
    
    return rol

@router.put("/{rol_id}", response_model=RolResponse)
async def update_rol(rol_id: str, rol: RolUpdate):
    """Actualizar un rol"""
    collection = get_collection("roles")
    
    if not ObjectId.is_valid(rol_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    update_data = {k: v for k, v in rol.dict(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay datos para actualizar")
    
    result = await collection.update_one(
        {"_id": ObjectId(rol_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
    
    updated_rol = await collection.find_one({"_id": ObjectId(rol_id)})
    return updated_rol

@router.delete("/{rol_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rol(rol_id: str):
    """Eliminar un rol"""
    collection = get_collection("roles")
    
    if not ObjectId.is_valid(rol_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.delete_one({"_id": ObjectId(rol_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
    
    return None

# Asignar rol a usuario
@router.post("/asignar", status_code=status.HTTP_201_CREATED)
async def asignar_rol_usuario(usuario_rol: UsuarioRol):
    """Asignar un rol a un usuario"""
    collection = get_collection("usuario_roles")
    
    # Verificar si ya existe la asignación
    existing = await collection.find_one({
        "usuario_id": usuario_rol.usuario_id,
        "rol_id": usuario_rol.rol_id
    })
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya tiene este rol asignado"
        )
    
    result = await collection.insert_one(usuario_rol.dict())
    return {"message": "Rol asignado exitosamente", "id": str(result.inserted_id)}

@router.delete("/remover", status_code=status.HTTP_204_NO_CONTENT)
async def remover_rol_usuario(usuario_rol: UsuarioRol):
    """Remover un rol de un usuario"""
    collection = get_collection("usuario_roles")
    
    result = await collection.delete_one({
        "usuario_id": usuario_rol.usuario_id,
        "rol_id": usuario_rol.rol_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asignación de rol no encontrada"
        )
    
    return None

@router.get("/usuario/{usuario_id}", response_model=List[RolResponse])
async def get_roles_usuario(usuario_id: str):
    """Obtener todos los roles de un usuario"""
    usuario_roles_collection = get_collection("usuario_roles")
    roles_collection = get_collection("roles")
    
    # Obtener asignaciones de roles del usuario
    asignaciones = await usuario_roles_collection.find({"usuario_id": usuario_id}).to_list(length=100)
    
    # Obtener los roles
    rol_ids = [ObjectId(a["rol_id"]) for a in asignaciones if ObjectId.is_valid(a["rol_id"])]
    roles = await roles_collection.find({"_id": {"$in": rol_ids}}).to_list(length=100)
    
    return roles
