from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from bson import ObjectId
from models.pedido import (
    PedidoCreate, PedidoUpdate, PedidoResponse,
    PedidoItemCreate, PedidoItemResponse
)
from database import get_collection

router = APIRouter()

# Función para serializar documentos de MongoDB (convertir ObjectId a string)
def serialize_doc(doc):
    """Convierte ObjectId a string en un documento"""
    if doc is None:
        return None
    if isinstance(doc, dict):
        result = {}
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                result[key] = str(value)
            elif isinstance(value, dict):
                result[key] = serialize_doc(value)
            elif isinstance(value, list):
                result[key] = [serialize_doc(item) if isinstance(item, (dict, ObjectId)) else item for item in value]
            else:
                result[key] = value
        return result
    elif isinstance(doc, ObjectId):
        return str(doc)
    return doc

def serialize_docs(docs):
    """Convierte una lista de documentos"""
    return [serialize_doc(doc) for doc in docs]

# ============= PEDIDOS =============

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_pedido(pedido: PedidoCreate):
    """Crear un nuevo pedido"""
    collection = get_collection("pedidos")
    
    pedido_dict = pedido.model_dump()
    result = await collection.insert_one(pedido_dict)
    created_pedido = await collection.find_one({"_id": result.inserted_id})
    
    return serialize_doc(created_pedido)

@router.get("/")
async def get_pedidos(
    skip: int = 0,
    limit: int = 100,
    usuario_id: Optional[str] = None,
    estado: Optional[str] = None
):
    """Obtener lista de pedidos"""
    collection = get_collection("pedidos")
    
    query = {}
    if usuario_id:
        query["usuario_id"] = usuario_id
    if estado:
        query["estado"] = estado
    
    pedidos = await collection.find(query).skip(skip).limit(limit).sort("creado_en", -1).to_list(length=limit)
    return serialize_docs(pedidos)

@router.get("/{pedido_id}")
async def get_pedido(pedido_id: str):
    """Obtener un pedido por ID"""
    collection = get_collection("pedidos")
    
    if not ObjectId.is_valid(pedido_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    pedido = await collection.find_one({"_id": ObjectId(pedido_id)})
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
    
    return serialize_doc(pedido)

@router.get("/usuario/{usuario_id}/historial")
async def get_historial_pedidos_usuario(usuario_id: str, skip: int = 0, limit: int = 50):
    """Obtener el historial de pedidos de un usuario"""
    collection = get_collection("pedidos")
    
    pedidos = await collection.find({"usuario_id": usuario_id}).skip(skip).limit(limit).sort("creado_en", -1).to_list(length=limit)
    return serialize_docs(pedidos)

@router.put("/{pedido_id}")
async def update_pedido(pedido_id: str, pedido: PedidoUpdate):
    """Actualizar un pedido"""
    collection = get_collection("pedidos")
    
    if not ObjectId.is_valid(pedido_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    update_data = {k: v for k, v in pedido.model_dump(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay datos para actualizar")
    
    result = await collection.update_one(
        {"_id": ObjectId(pedido_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
    
    updated_pedido = await collection.find_one({"_id": ObjectId(pedido_id)})
    return serialize_doc(updated_pedido)

@router.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pedido(pedido_id: str):
    """Eliminar (cancelar) un pedido"""
    collection = get_collection("pedidos")
    
    if not ObjectId.is_valid(pedido_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    # Cambiar estado a cancelado en lugar de eliminar
    result = await collection.update_one(
        {"_id": ObjectId(pedido_id)},
        {"$set": {"estado": "cancelado"}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
    
    return None

# ============= ITEMS DEL PEDIDO =============

@router.post("/{pedido_id}/items", status_code=status.HTTP_201_CREATED)
async def add_item_pedido(pedido_id: str, item: PedidoItemCreate):
    """Agregar un item al pedido"""
    items_collection = get_collection("pedido_items")
    pedidos_collection = get_collection("pedidos")
    
    # Verificar que el pedido existe
    if not ObjectId.is_valid(pedido_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de pedido inválido")
    
    pedido = await pedidos_collection.find_one({"_id": ObjectId(pedido_id)})
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
    
    item_dict = item.model_dump()
    item_dict["pedido_id"] = pedido_id
    
    result = await items_collection.insert_one(item_dict)
    created_item = await items_collection.find_one({"_id": result.inserted_id})
    
    return serialize_doc(created_item)

@router.get("/{pedido_id}/items")
async def get_items_pedido(pedido_id: str):
    """Obtener todos los items de un pedido"""
    collection = get_collection("pedido_items")
    
    items = await collection.find({"pedido_id": pedido_id}).to_list(length=100)
    return serialize_docs(items)
