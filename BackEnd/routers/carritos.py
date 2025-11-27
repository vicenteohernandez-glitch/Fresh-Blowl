from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from bson import ObjectId
from models.carrito import (
    CarritoCreate, CarritoUpdate, CarritoResponse,
    CarritoItemCreate, CarritoItemUpdate, CarritoItemResponse
)
from database import get_collection
from datetime import datetime

router = APIRouter()

# ============= CARRITOS =============

@router.post("/", response_model=CarritoResponse, status_code=status.HTTP_201_CREATED)
async def create_carrito(carrito: CarritoCreate):
    """Crear un nuevo carrito"""
    collection = get_collection("carritos")
    
    carrito_dict = carrito.dict()
    carrito_dict["actualizado_en"] = datetime.utcnow()
    
    result = await collection.insert_one(carrito_dict)
    created_carrito = await collection.find_one({"_id": result.inserted_id})
    
    return created_carrito

@router.get("/", response_model=List[CarritoResponse])
async def get_carritos(skip: int = 0, limit: int = 100, usuario_id: Optional[str] = None):
    """Obtener lista de carritos"""
    collection = get_collection("carritos")
    
    query = {}
    if usuario_id:
        query["usuario_id"] = usuario_id
    
    carritos = await collection.find(query).skip(skip).limit(limit).to_list(length=limit)
    return carritos

@router.get("/{carrito_id}", response_model=CarritoResponse)
async def get_carrito(carrito_id: str):
    """Obtener un carrito por ID"""
    collection = get_collection("carritos")
    
    if not ObjectId.is_valid(carrito_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    carrito = await collection.find_one({"_id": ObjectId(carrito_id)})
    if not carrito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado")
    
    return carrito

@router.get("/usuario/{usuario_id}/activo", response_model=CarritoResponse)
async def get_carrito_activo_usuario(usuario_id: str):
    """Obtener el carrito activo de un usuario"""
    collection = get_collection("carritos")
    
    carrito = await collection.find_one({
        "usuario_id": usuario_id,
        "estado": "activo"
    })
    
    if not carrito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito activo no encontrado")
    
    return carrito

@router.put("/{carrito_id}", response_model=CarritoResponse)
async def update_carrito(carrito_id: str, carrito: CarritoUpdate):
    """Actualizar un carrito"""
    collection = get_collection("carritos")
    
    if not ObjectId.is_valid(carrito_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    update_data = {k: v for k, v in carrito.dict(exclude_unset=True).items() if v is not None}
    update_data["actualizado_en"] = datetime.utcnow()
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay datos para actualizar")
    
    result = await collection.update_one(
        {"_id": ObjectId(carrito_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado")
    
    updated_carrito = await collection.find_one({"_id": ObjectId(carrito_id)})
    return updated_carrito

@router.delete("/{carrito_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_carrito(carrito_id: str):
    """Eliminar un carrito"""
    collection = get_collection("carritos")
    
    if not ObjectId.is_valid(carrito_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.delete_one({"_id": ObjectId(carrito_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado")
    
    return None

# ============= ITEMS DEL CARRITO =============

@router.post("/{carrito_id}/items", response_model=CarritoItemResponse, status_code=status.HTTP_201_CREATED)
async def add_item_carrito(carrito_id: str, item: CarritoItemCreate):
    """Agregar un item al carrito"""
    items_collection = get_collection("carrito_items")
    carritos_collection = get_collection("carritos")
    
    # Verificar que el carrito existe
    if not ObjectId.is_valid(carrito_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de carrito inválido")
    
    carrito = await carritos_collection.find_one({"_id": ObjectId(carrito_id)})
    if not carrito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado")
    
    item_dict = item.dict()
    item_dict["carrito_id"] = carrito_id
    
    result = await items_collection.insert_one(item_dict)
    created_item = await items_collection.find_one({"_id": result.inserted_id})
    
    # Actualizar timestamp del carrito
    await carritos_collection.update_one(
        {"_id": ObjectId(carrito_id)},
        {"$set": {"actualizado_en": datetime.utcnow()}}
    )
    
    return created_item

@router.get("/{carrito_id}/items", response_model=List[CarritoItemResponse])
async def get_items_carrito(carrito_id: str):
    """Obtener todos los items de un carrito"""
    collection = get_collection("carrito_items")
    
    items = await collection.find({"carrito_id": carrito_id}).to_list(length=100)
    return items

@router.put("/items/{item_id}", response_model=CarritoItemResponse)
async def update_item_carrito(item_id: str, item: CarritoItemUpdate):
    """Actualizar un item del carrito"""
    collection = get_collection("carrito_items")
    
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    update_data = {k: v for k, v in item.dict(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay datos para actualizar")
    
    result = await collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
    
    updated_item = await collection.find_one({"_id": ObjectId(item_id)})
    
    # Actualizar timestamp del carrito
    carritos_collection = get_collection("carritos")
    await carritos_collection.update_one(
        {"_id": ObjectId(updated_item["carrito_id"])},
        {"$set": {"actualizado_en": datetime.utcnow()}}
    )
    
    return updated_item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_carrito(item_id: str):
    """Eliminar un item del carrito"""
    collection = get_collection("carrito_items")
    
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    # Obtener el item antes de eliminarlo
    item = await collection.find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
    
    result = await collection.delete_one({"_id": ObjectId(item_id)})
    
    # Actualizar timestamp del carrito
    carritos_collection = get_collection("carritos")
    await carritos_collection.update_one(
        {"_id": ObjectId(item["carrito_id"])},
        {"$set": {"actualizado_en": datetime.utcnow()}}
    )
    
    return None
