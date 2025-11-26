from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from bson import ObjectId
from api.models.producto import (
    ProductoCreate, ProductoUpdate, ProductoResponse,
    VarianteCreate, VarianteUpdate, VarianteResponse
)
from api.database import get_collection

router = APIRouter()

# ============= PRODUCTOS =============

@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def create_producto(producto: ProductoCreate):
    """Crear un nuevo producto"""
    collection = get_collection("productos")
    
    producto_dict = producto.dict()
    result = await collection.insert_one(producto_dict)
    created_producto = await collection.find_one({"_id": result.inserted_id})
    
    return created_producto

@router.get("/", response_model=List[ProductoResponse])
async def get_productos(
    skip: int = 0,
    limit: int = 100,
    categoria_id: Optional[str] = None,
    activo: Optional[bool] = None,
    agotado: Optional[bool] = None
):
    """Obtener lista de productos"""
    collection = get_collection("productos")
    
    query = {}
    if categoria_id:
        query["categoria_id"] = categoria_id
    if activo is not None:
        query["activo"] = activo
    if agotado is not None:
        query["agotado"] = agotado
    
    productos = await collection.find(query).skip(skip).limit(limit).to_list(length=limit)
    return productos

@router.get("/{producto_id}", response_model=ProductoResponse)
async def get_producto(producto_id: str):
    """Obtener un producto por ID"""
    collection = get_collection("productos")
    
    if not ObjectId.is_valid(producto_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    producto = await collection.find_one({"_id": ObjectId(producto_id)})
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    
    return producto

@router.put("/{producto_id}", response_model=ProductoResponse)
async def update_producto(producto_id: str, producto: ProductoUpdate):
    """Actualizar un producto"""
    collection = get_collection("productos")
    
    if not ObjectId.is_valid(producto_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    update_data = {k: v for k, v in producto.dict(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay datos para actualizar")
    
    result = await collection.update_one(
        {"_id": ObjectId(producto_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    
    updated_producto = await collection.find_one({"_id": ObjectId(producto_id)})
    return updated_producto

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_producto(producto_id: str):
    """Eliminar un producto"""
    collection = get_collection("productos")
    
    if not ObjectId.is_valid(producto_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.delete_one({"_id": ObjectId(producto_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    
    return None

# ============= VARIANTES =============

@router.post("/{producto_id}/variantes", response_model=VarianteResponse, status_code=status.HTTP_201_CREATED)
async def create_variante(producto_id: str, variante: VarianteCreate):
    """Crear una variante para un producto"""
    collection = get_collection("variantes")
    
    # Verificar que el producto existe
    productos_collection = get_collection("productos")
    if not ObjectId.is_valid(producto_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de producto inválido")
    
    producto = await productos_collection.find_one({"_id": ObjectId(producto_id)})
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    
    variante_dict = variante.dict()
    variante_dict["producto_id"] = producto_id
    
    result = await collection.insert_one(variante_dict)
    created_variante = await collection.find_one({"_id": result.inserted_id})
    
    return created_variante

@router.get("/{producto_id}/variantes", response_model=List[VarianteResponse])
async def get_variantes_producto(producto_id: str):
    """Obtener todas las variantes de un producto"""
    collection = get_collection("variantes")
    
    variantes = await collection.find({"producto_id": producto_id}).to_list(length=100)
    return variantes

@router.put("/variantes/{variante_id}", response_model=VarianteResponse)
async def update_variante(variante_id: str, variante: VarianteUpdate):
    """Actualizar una variante"""
    collection = get_collection("variantes")
    
    if not ObjectId.is_valid(variante_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    update_data = {k: v for k, v in variante.dict(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay datos para actualizar")
    
    result = await collection.update_one(
        {"_id": ObjectId(variante_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variante no encontrada")
    
    updated_variante = await collection.find_one({"_id": ObjectId(variante_id)})
    return updated_variante

@router.delete("/variantes/{variante_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_variante(variante_id: str):
    """Eliminar una variante"""
    collection = get_collection("variantes")
    
    if not ObjectId.is_valid(variante_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.delete_one({"_id": ObjectId(variante_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variante no encontrada")
    
    return None
