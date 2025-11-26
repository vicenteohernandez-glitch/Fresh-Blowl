from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from bson import ObjectId
from api.models.pago import PagoCreate, PagoUpdate, PagoResponse
from api.database import get_collection

router = APIRouter()

@router.post("/", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
async def create_pago(pago: PagoCreate):
    """Crear un nuevo pago"""
    collection = get_collection("pagos")
    
    pago_dict = pago.dict()
    result = await collection.insert_one(pago_dict)
    created_pago = await collection.find_one({"_id": result.inserted_id})
    
    return created_pago

@router.get("/", response_model=List[PagoResponse])
async def get_pagos(skip: int = 0, limit: int = 100, pedido_id: Optional[str] = None, estado: Optional[str] = None):
    """Obtener lista de pagos"""
    collection = get_collection("pagos")
    
    query = {}
    if pedido_id:
        query["pedido_id"] = pedido_id
    if estado:
        query["estado"] = estado
    
    pagos = await collection.find(query).skip(skip).limit(limit).to_list(length=limit)
    return pagos

@router.get("/{pago_id}", response_model=PagoResponse)
async def get_pago(pago_id: str):
    """Obtener un pago por ID"""
    collection = get_collection("pagos")
    
    if not ObjectId.is_valid(pago_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    pago = await collection.find_one({"_id": ObjectId(pago_id)})
    if not pago:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
    
    return pago

@router.get("/pedido/{pedido_id}", response_model=PagoResponse)
async def get_pago_by_pedido(pedido_id: str):
    """Obtener el pago de un pedido"""
    collection = get_collection("pagos")
    
    pago = await collection.find_one({"pedido_id": pedido_id})
    if not pago:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado para este pedido")
    
    return pago

@router.put("/{pago_id}", response_model=PagoResponse)
async def update_pago(pago_id: str, pago: PagoUpdate):
    """Actualizar un pago"""
    collection = get_collection("pagos")
    
    if not ObjectId.is_valid(pago_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    update_data = {k: v for k, v in pago.dict(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay datos para actualizar")
    
    result = await collection.update_one(
        {"_id": ObjectId(pago_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
    
    updated_pago = await collection.find_one({"_id": ObjectId(pago_id)})
    return updated_pago

@router.post("/{pago_id}/aprobar", response_model=PagoResponse)
async def aprobar_pago(pago_id: str):
    """Aprobar un pago"""
    collection = get_collection("pagos")
    
    if not ObjectId.is_valid(pago_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.update_one(
        {"_id": ObjectId(pago_id)},
        {"$set": {"estado": "aprobado"}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
    
    updated_pago = await collection.find_one({"_id": ObjectId(pago_id)})
    return updated_pago

@router.post("/{pago_id}/rechazar", response_model=PagoResponse)
async def rechazar_pago(pago_id: str):
    """Rechazar un pago"""
    collection = get_collection("pagos")
    
    if not ObjectId.is_valid(pago_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.update_one(
        {"_id": ObjectId(pago_id)},
        {"$set": {"estado": "rechazado"}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
    
    updated_pago = await collection.find_one({"_id": ObjectId(pago_id)})
    return updated_pago

@router.delete("/{pago_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pago(pago_id: str):
    """Eliminar un pago"""
    collection = get_collection("pagos")
    
    if not ObjectId.is_valid(pago_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.delete_one({"_id": ObjectId(pago_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
    
    return None
