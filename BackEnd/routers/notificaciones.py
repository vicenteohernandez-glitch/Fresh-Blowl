from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from models.notificacion import NotificacionCreate, NotificacionUpdate, NotificacionResponse
from database import get_collection
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=NotificacionResponse, status_code=status.HTTP_201_CREATED)
async def create_notificacion(notificacion: NotificacionCreate):
    """Crear una nueva notificación"""
    collection = get_collection("notificaciones")
    
    notificacion_dict = notificacion.dict()
    result = await collection.insert_one(notificacion_dict)
    created_notificacion = await collection.find_one({"_id": result.inserted_id})
    
    return created_notificacion

@router.get("/", response_model=List[NotificacionResponse])
async def get_notificaciones(skip: int = 0, limit: int = 100, usuario_id: str = None, estado: str = None):
    """Obtener lista de notificaciones"""
    collection = get_collection("notificaciones")
    
    query = {}
    if usuario_id:
        query["usuario_id"] = usuario_id
    if estado:
        query["estado"] = estado
    
    notificaciones = await collection.find(query).skip(skip).limit(limit).to_list(length=limit)
    return notificaciones

@router.get("/{notificacion_id}", response_model=NotificacionResponse)
async def get_notificacion(notificacion_id: str):
    """Obtener una notificación por ID"""
    collection = get_collection("notificaciones")
    
    if not ObjectId.is_valid(notificacion_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    notificacion = await collection.find_one({"_id": ObjectId(notificacion_id)})
    if not notificacion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notificación no encontrada")
    
    return notificacion

@router.put("/{notificacion_id}", response_model=NotificacionResponse)
async def update_notificacion(notificacion_id: str, notificacion: NotificacionUpdate):
    """Actualizar una notificación"""
    collection = get_collection("notificaciones")
    
    if not ObjectId.is_valid(notificacion_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    update_data = {k: v for k, v in notificacion.dict(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay datos para actualizar")
    
    # Si se marca como enviado, actualizar la fecha
    if update_data.get("estado") == "enviado":
        update_data["enviado_en"] = datetime.utcnow()
    
    result = await collection.update_one(
        {"_id": ObjectId(notificacion_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notificación no encontrada")
    
    updated_notificacion = await collection.find_one({"_id": ObjectId(notificacion_id)})
    return updated_notificacion

@router.post("/{notificacion_id}/marcar-enviada", response_model=NotificacionResponse)
async def marcar_notificacion_enviada(notificacion_id: str):
    """Marcar una notificación como enviada"""
    collection = get_collection("notificaciones")
    
    if not ObjectId.is_valid(notificacion_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.update_one(
        {"_id": ObjectId(notificacion_id)},
        {"$set": {"estado": "enviado", "enviado_en": datetime.utcnow()}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notificación no encontrada")
    
    updated_notificacion = await collection.find_one({"_id": ObjectId(notificacion_id)})
    return updated_notificacion

@router.delete("/{notificacion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notificacion(notificacion_id: str):
    """Eliminar una notificación"""
    collection = get_collection("notificaciones")
    
    if not ObjectId.is_valid(notificacion_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.delete_one({"_id": ObjectId(notificacion_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notificación no encontrada")
    
    return None
