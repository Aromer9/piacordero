from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from bson import ObjectId

from app.config import get_db
from app.auth import require_admin
from app.models.product import (
    ProductCreate,
    ProductUpdate,
    product_doc,
    serialize_product,
    Category,
)

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("")
async def list_products(
    category: Optional[Category] = Query(None),
    featured: Optional[bool] = Query(None),
):
    db = get_db()
    query: dict = {}
    if category:
        query["category"] = category.value
    if featured is not None:
        query["featured"] = featured

    cursor = db.products.find(query).sort("order", 1)
    products = []
    async for doc in cursor:
        products.append(serialize_product(doc))
    return products


@router.get("/{product_id}")
async def get_product(product_id: str):
    db = get_db()
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    doc = await db.products.find_one({"_id": ObjectId(product_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return serialize_product(doc)


@router.post("", status_code=201, dependencies=[Depends(require_admin)])
async def create_product(data: ProductCreate):
    db = get_db()
    doc = product_doc(data)
    result = await db.products.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return doc


@router.put("/{product_id}", dependencies=[Depends(require_admin)])
async def update_product(product_id: str, data: ProductUpdate):
    db = get_db()
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    def _int(v):
        return int(v) if v is not None else None

    # Mapeo explícito campo a campo: evita que el loop excluya precios null o None.
    # image_url llega ya normalizada por BeforeValidator (None o string no vacío).
    update_data: dict = {
        "image_url":  data.image_url,
        "badge":      data.badge,
        "price":        _int(data.price),
        "price_8_10p":  _int(data.price_8_10p),
        "price_15p":    _int(data.price_15p),
        "price_20p":    _int(data.price_20p),
        "price_30p":    _int(data.price_30p),
    }
    # Campos obligatorios: solo se actualizan si vienen con valor
    if data.name:
        update_data["name"] = data.name
    if data.description is not None:
        update_data["description"] = data.description
    if data.category is not None:
        update_data["category"] = data.category.value if isinstance(data.category, Category) else data.category
    if data.featured is not None:
        update_data["featured"] = data.featured
    if data.order is not None:
        update_data["order"] = int(data.order)

    result = await db.products.update_one(
        {"_id": ObjectId(product_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    doc = await db.products.find_one({"_id": ObjectId(product_id)})
    return serialize_product(doc)


@router.patch("/{product_id}/order", dependencies=[Depends(require_admin)])
async def update_order(product_id: str, body: dict):
    db = get_db()
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    await db.products.update_one(
        {"_id": ObjectId(product_id)}, {"$set": {"order": body.get("order", 0)}}
    )
    return {"ok": True}


@router.delete("/{product_id}", status_code=204, dependencies=[Depends(require_admin)])
async def delete_product(product_id: str):
    db = get_db()
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    result = await db.products.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
