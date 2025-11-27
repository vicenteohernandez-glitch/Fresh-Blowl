from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from models.comprobante import ComprobanteCreate, ComprobanteUpdate, ComprobanteResponse
from database import get_collection

router = APIRouter()

@router.post("/", response_model=ComprobanteResponse, status_code=status.HTTP_201_CREATED)
async def create_comprobante(comprobante: ComprobanteCreate):
    """Crear un nuevo comprobante"""
    collection = get_collection("comprobantes")
    
    comprobante_dict = comprobante.dict()
    result = await collection.insert_one(comprobante_dict)
    created_comprobante = await collection.find_one({"_id": result.inserted_id})
    
    return created_comprobante

@router.get("/", response_model=List[ComprobanteResponse])
async def get_comprobantes(skip: int = 0, limit: int = 100, tipo: str = None):
    """Obtener lista de comprobantes"""
    collection = get_collection("comprobantes")
    
    query = {}
    if tipo:
        query["tipo"] = tipo
    
    comprobantes = await collection.find(query).skip(skip).limit(limit).to_list(length=limit)
    return comprobantes

@router.get("/{comprobante_id}", response_model=ComprobanteResponse)
async def get_comprobante(comprobante_id: str):
    """Obtener un comprobante por ID"""
    collection = get_collection("comprobantes")
    
    if not ObjectId.is_valid(comprobante_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    comprobante = await collection.find_one({"_id": ObjectId(comprobante_id)})
    if not comprobante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comprobante no encontrado")
    
    return comprobante

@router.get("/pedido/{pedido_id}", response_model=ComprobanteResponse)
async def get_comprobante_by_pedido(pedido_id: str):
    """Obtener el comprobante de un pedido"""
    collection = get_collection("comprobantes")
    
    comprobante = await collection.find_one({"pedido_id": pedido_id})
    if not comprobante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comprobante no encontrado para este pedido")
    
    return comprobante

@router.get("/numero/{numero}", response_model=ComprobanteResponse)
async def get_comprobante_by_numero(numero: str):
    """Obtener un comprobante por número"""
    collection = get_collection("comprobantes")
    
    comprobante = await collection.find_one({"numero": numero})
    if not comprobante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comprobante no encontrado")
    
    return comprobante

@router.put("/{comprobante_id}", response_model=ComprobanteResponse)
async def update_comprobante(comprobante_id: str, comprobante: ComprobanteUpdate):
    """Actualizar un comprobante"""
    collection = get_collection("comprobantes")
    
    if not ObjectId.is_valid(comprobante_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    update_data = {k: v for k, v in comprobante.dict(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay datos para actualizar")
    
    result = await collection.update_one(
        {"_id": ObjectId(comprobante_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comprobante no encontrado")
    
    updated_comprobante = await collection.find_one({"_id": ObjectId(comprobante_id)})
    return updated_comprobante

@router.delete("/{comprobante_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comprobante(comprobante_id: str):
    """Eliminar un comprobante"""
    collection = get_collection("comprobantes")
    
    if not ObjectId.is_valid(comprobante_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.delete_one({"_id": ObjectId(comprobante_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comprobante no encontrado")
    
    return None
