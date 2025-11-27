from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from models.direccion import DireccionCreate, DireccionUpdate, DireccionResponse
from database import get_collection

router = APIRouter()

@router.post("/", response_model=DireccionResponse, status_code=status.HTTP_201_CREATED)
async def create_direccion(direccion: DireccionCreate):
    """Crear una nueva dirección"""
    collection = get_collection("direcciones")
    
    direccion_dict = direccion.dict()
    result = await collection.insert_one(direccion_dict)
    created_direccion = await collection.find_one({"_id": result.inserted_id})
    
    return created_direccion

@router.get("/", response_model=List[DireccionResponse])
async def get_direcciones(skip: int = 0, limit: int = 100, usuario_id: str = None):
    """Obtener lista de direcciones"""
    collection = get_collection("direcciones")
    
    query = {}
    if usuario_id:
        query["usuario_id"] = usuario_id
    
    direcciones = await collection.find(query).skip(skip).limit(limit).to_list(length=limit)
    return direcciones

@router.get("/{direccion_id}", response_model=DireccionResponse)
async def get_direccion(direccion_id: str):
    """Obtener una dirección por ID"""
    collection = get_collection("direcciones")
    
    if not ObjectId.is_valid(direccion_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    direccion = await collection.find_one({"_id": ObjectId(direccion_id)})
    if not direccion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dirección no encontrada")
    
    return direccion

@router.get("/usuario/{usuario_id}/favorita", response_model=DireccionResponse)
async def get_direccion_favorita(usuario_id: str):
    """Obtener la dirección favorita de un usuario"""
    collection = get_collection("direcciones")
    
    direccion = await collection.find_one({
        "usuario_id": usuario_id,
        "favorita": True
    })
    
    if not direccion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dirección favorita no encontrada")
    
    return direccion

@router.put("/{direccion_id}", response_model=DireccionResponse)
async def update_direccion(direccion_id: str, direccion: DireccionUpdate):
    """Actualizar una dirección"""
    collection = get_collection("direcciones")
    
    if not ObjectId.is_valid(direccion_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    update_data = {k: v for k, v in direccion.dict(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay datos para actualizar")
    
    # Si se marca como favorita, quitar favorita de las demás direcciones del usuario
    if update_data.get("favorita"):
        direccion_actual = await collection.find_one({"_id": ObjectId(direccion_id)})
        if direccion_actual:
            await collection.update_many(
                {"usuario_id": direccion_actual["usuario_id"], "_id": {"$ne": ObjectId(direccion_id)}},
                {"$set": {"favorita": False}}
            )
    
    result = await collection.update_one(
        {"_id": ObjectId(direccion_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dirección no encontrada")
    
    updated_direccion = await collection.find_one({"_id": ObjectId(direccion_id)})
    return updated_direccion

@router.delete("/{direccion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_direccion(direccion_id: str):
    """Eliminar una dirección"""
    collection = get_collection("direcciones")
    
    if not ObjectId.is_valid(direccion_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.delete_one({"_id": ObjectId(direccion_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dirección no encontrada")
    
    return None
