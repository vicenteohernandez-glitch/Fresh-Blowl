from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from models.cupon import CuponCreate, CuponUpdate, CuponResponse
from database import get_collection
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=CuponResponse, status_code=status.HTTP_201_CREATED)
async def create_cupon(cupon: CuponCreate):
    """Crear un nuevo cupón"""
    collection = get_collection("cupones")
    
    # Verificar que el código no exista
    existing = await collection.find_one({"codigo": cupon.codigo})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El código de cupón ya existe"
        )
    
    cupon_dict = cupon.dict()
    result = await collection.insert_one(cupon_dict)
    created_cupon = await collection.find_one({"_id": result.inserted_id})
    
    return created_cupon

@router.get("/", response_model=List[CuponResponse])
async def get_cupones(skip: int = 0, limit: int = 100, activo: bool = None):
    """Obtener lista de cupones"""
    collection = get_collection("cupones")
    
    query = {}
    if activo is not None:
        query["activo"] = activo
    
    cupones = await collection.find(query).skip(skip).limit(limit).to_list(length=limit)
    return cupones

@router.get("/{cupon_id}", response_model=CuponResponse)
async def get_cupon(cupon_id: str):
    """Obtener un cupón por ID"""
    collection = get_collection("cupones")
    
    if not ObjectId.is_valid(cupon_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    cupon = await collection.find_one({"_id": ObjectId(cupon_id)})
    if not cupon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cupón no encontrado")
    
    return cupon

@router.get("/codigo/{codigo}", response_model=CuponResponse)
async def get_cupon_by_codigo(codigo: str):
    """Obtener un cupón por código"""
    collection = get_collection("cupones")
    
    cupon = await collection.find_one({"codigo": codigo})
    if not cupon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cupón no encontrado")
    
    return cupon

@router.post("/validar/{codigo}")
async def validar_cupon(codigo: str):
    """Validar si un cupón es válido para usar"""
    collection = get_collection("cupones")
    
    cupon = await collection.find_one({"codigo": codigo})
    if not cupon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cupón no encontrado")
    
    # Verificar si está activo
    if not cupon.get("activo", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cupón inactivo"
        )
    
    # Verificar fechas
    ahora = datetime.utcnow()
    if cupon.get("valido_desde") and cupon["valido_desde"] > ahora:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cupón aún no válido"
        )
    
    if cupon.get("valido_hasta") and cupon["valido_hasta"] < ahora:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cupón expirado"
        )
    
    # Verificar uso máximo
    uso_maximo = cupon.get("uso_maximo", 0)
    uso_actual = cupon.get("uso_actual", 0)
    
    if uso_maximo > 0 and uso_actual >= uso_maximo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cupón agotado"
        )
    
    return {
        "valido": True,
        "descuento_porcentaje": cupon.get("descuento_porcentaje", 0),
        "descuento_fijo": cupon.get("descuento_fijo", 0)
    }

@router.put("/{cupon_id}", response_model=CuponResponse)
async def update_cupon(cupon_id: str, cupon: CuponUpdate):
    """Actualizar un cupón"""
    collection = get_collection("cupones")
    
    if not ObjectId.is_valid(cupon_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    update_data = {k: v for k, v in cupon.dict(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay datos para actualizar")
    
    result = await collection.update_one(
        {"_id": ObjectId(cupon_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cupón no encontrado")
    
    updated_cupon = await collection.find_one({"_id": ObjectId(cupon_id)})
    return updated_cupon

@router.post("/{cupon_id}/usar", status_code=status.HTTP_200_OK)
async def usar_cupon(cupon_id: str):
    """Incrementar el contador de uso de un cupón"""
    collection = get_collection("cupones")
    
    if not ObjectId.is_valid(cupon_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.update_one(
        {"_id": ObjectId(cupon_id)},
        {"$inc": {"uso_actual": 1}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cupón no encontrado")
    
    return {"message": "Cupón usado exitosamente"}

@router.delete("/{cupon_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cupon(cupon_id: str):
    """Eliminar un cupón"""
    collection = get_collection("cupones")
    
    if not ObjectId.is_valid(cupon_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.delete_one({"_id": ObjectId(cupon_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cupón no encontrado")
    
    return None
