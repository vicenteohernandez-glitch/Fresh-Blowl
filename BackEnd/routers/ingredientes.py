from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from models.ingrediente import (
    IngredienteCreate, IngredienteUpdate, IngredienteResponse,
    ProductoIngredienteCreate, ProductoIngredienteResponse
)
from database import get_collection

router = APIRouter()

def serialize_doc(doc):
    """Serializa un documento MongoDB convirtiendo ObjectId a string"""
    if doc is None:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

# ============= INGREDIENTES =============

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_ingrediente(ingrediente: IngredienteCreate):
    """Crear un nuevo ingrediente"""
    collection = get_collection("ingredientes")
    
    ingrediente_dict = ingrediente.model_dump()
    result = await collection.insert_one(ingrediente_dict)
    created_ingrediente = await collection.find_one({"_id": result.inserted_id})
    
    return serialize_doc(created_ingrediente)

@router.get("/", response_model=List[dict])
async def get_ingredientes(skip: int = 0, limit: int = 100, adicional: bool = None, disponible: bool = None, bajo_stock: bool = None):
    """Obtener lista de ingredientes"""
    collection = get_collection("ingredientes")
    
    query = {}
    if adicional is not None:
        query["adicional"] = adicional
    if disponible is not None:
        query["disponible"] = disponible
    
    ingredientes = await collection.find(query).skip(skip).limit(limit).to_list(length=limit)
    result = [serialize_doc(ing) for ing in ingredientes]
    
    # Filtrar por bajo stock si se solicita
    if bajo_stock:
        result = [ing for ing in result if ing.get("stock", 100) <= ing.get("stock_minimo", 10)]
    
    return result

@router.get("/alertas", response_model=List[dict])
async def get_alertas_stock():
    """Obtener ingredientes con stock bajo o agotados"""
    collection = get_collection("ingredientes")
    
    # Obtener todos los ingredientes
    ingredientes = await collection.find({}).to_list(length=1000)
    alertas = []
    
    for ing in ingredientes:
        stock = ing.get("stock", 100)
        stock_minimo = ing.get("stock_minimo", 10)
        
        if stock <= 0:
            ing["alerta"] = "agotado"
            alertas.append(serialize_doc(ing))
        elif stock <= stock_minimo:
            ing["alerta"] = "bajo"
            alertas.append(serialize_doc(ing))
    
    return alertas

@router.get("/{ingrediente_id}", response_model=dict)
async def get_ingrediente(ingrediente_id: str):
    """Obtener un ingrediente por ID"""
    collection = get_collection("ingredientes")
    
    if not ObjectId.is_valid(ingrediente_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    ingrediente = await collection.find_one({"_id": ObjectId(ingrediente_id)})
    if not ingrediente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado")
    
    return serialize_doc(ingrediente)

@router.put("/{ingrediente_id}", response_model=dict)
async def update_ingrediente(ingrediente_id: str, ingrediente: IngredienteUpdate):
    """Actualizar un ingrediente"""
    collection = get_collection("ingredientes")
    
    if not ObjectId.is_valid(ingrediente_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    update_data = {k: v for k, v in ingrediente.model_dump(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay datos para actualizar")
    
    result = await collection.update_one(
        {"_id": ObjectId(ingrediente_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        existing = await collection.find_one({"_id": ObjectId(ingrediente_id)})
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado")
    
    updated_ingrediente = await collection.find_one({"_id": ObjectId(ingrediente_id)})
    return serialize_doc(updated_ingrediente)

@router.delete("/{ingrediente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ingrediente(ingrediente_id: str):
    """Eliminar un ingrediente"""
    collection = get_collection("ingredientes")
    
    if not ObjectId.is_valid(ingrediente_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.delete_one({"_id": ObjectId(ingrediente_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado")
    
    return None

# ============= PRODUCTO-INGREDIENTE =============

@router.post("/producto-ingrediente", response_model=ProductoIngredienteResponse, status_code=status.HTTP_201_CREATED)
async def create_producto_ingrediente(relacion: ProductoIngredienteCreate):
    """Asociar un ingrediente a un producto"""
    collection = get_collection("producto_ingredientes")
    
    # Verificar que producto e ingrediente existen
    productos_collection = get_collection("productos")
    ingredientes_collection = get_collection("ingredientes")
    
    if ObjectId.is_valid(relacion.producto_id):
        producto = await productos_collection.find_one({"_id": ObjectId(relacion.producto_id)})
    else:
        producto = None
    
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    
    if ObjectId.is_valid(relacion.ingrediente_id):
        ingrediente = await ingredientes_collection.find_one({"_id": ObjectId(relacion.ingrediente_id)})
    else:
        ingrediente = None
    
    if not ingrediente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado")
    
    relacion_dict = relacion.dict()
    result = await collection.insert_one(relacion_dict)
    created_relacion = await collection.find_one({"_id": result.inserted_id})
    
    return created_relacion

@router.get("/producto/{producto_id}/ingredientes", response_model=List[ProductoIngredienteResponse])
async def get_ingredientes_producto(producto_id: str):
    """Obtener todos los ingredientes de un producto"""
    collection = get_collection("producto_ingredientes")
    
    relaciones = await collection.find({"producto_id": producto_id}).to_list(length=100)
    return relaciones

@router.delete("/producto-ingrediente/{relacion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_producto_ingrediente(relacion_id: str):
    """Eliminar la asociación de un ingrediente con un producto"""
    collection = get_collection("producto_ingredientes")
    
    if not ObjectId.is_valid(relacion_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.delete_one({"_id": ObjectId(relacion_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relación no encontrada")
    
    return None
