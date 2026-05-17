from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated, Optional, Any
from datetime import datetime, timezone
from enum import Enum


class Category(str, Enum):
    tortas = "tortas"
    tartas = "tartas"
    petit_fours = "petit_fours"
    temporada = "temporada"


def _normalize_optional_image(v: Any) -> str | None:
    """Acepta null, '', o string; evita error de validación con JSON null."""
    if v is None:
        return None
    if isinstance(v, str):
        s = v.strip()
        return s if s else None
    return None


# Normaliza imagen antes del chequeo de tipos (null / "" → None)
OptionalImageUrl = Annotated[str | None, BeforeValidator(_normalize_optional_image)]


class ProductCreate(BaseModel):
    name: str
    description: str
    category: Category
    image_url: OptionalImageUrl = None
    featured: bool = False
    sold_out: bool = False
    order: int = 0
    price: int | None = None
    price_8_10p: int | None = None
    price_15p: int | None = None
    price_20p: int | None = None
    price_30p: int | None = None
    badge: str | None = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[Category] = None
    image_url: OptionalImageUrl = None
    featured: Optional[bool] = None
    sold_out: Optional[bool] = None
    order: Optional[int] = None
    price: Optional[int] = None
    price_8_10p: Optional[int] = None
    price_15p: Optional[int] = None
    price_20p: Optional[int] = None
    price_30p: Optional[int] = None
    badge: Optional[str] = None


class ProductOut(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: str
    category: Category
    image_url: Optional[str] = None
    featured: bool
    sold_out: bool = False
    order: int
    price: Optional[int] = None
    price_8_10p: Optional[int] = None
    price_15p: Optional[int] = None
    price_20p: Optional[int] = None
    price_30p: Optional[int] = None
    badge: Optional[str] = None
    created_at: datetime

    model_config = {"populate_by_name": True}


def product_doc(data: ProductCreate) -> dict:
    d = data.model_dump()
    cat = d.get("category")
    if isinstance(cat, Enum):
        d["category"] = cat.value
    img = d.get("image_url")
    if img is not None and isinstance(img, str):
        img = img.strip()
    d["image_url"] = img or None
    tiers = [
        d.get("price_8_10p"),
        d.get("price_15p"),
        d.get("price_20p"),
        d.get("price_30p"),
    ]
    tiers_ok = [x for x in tiers if x is not None]
    if tiers_ok and d.get("price") is None:
        d["price"] = min(int(x) for x in tiers_ok)
    for key in ("price", "price_8_10p", "price_15p", "price_20p", "price_30p"):
        v = d.get(key)
        if v is not None:
            d[key] = int(v)
    d["created_at"] = datetime.now(timezone.utc)
    return d


def serialize_product(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    for key in ("price", "price_8_10p", "price_15p", "price_20p", "price_30p"):
        if key in doc and doc[key] is not None:
            doc[key] = int(doc[key])
    doc["sold_out"] = bool(doc.get("sold_out"))
    return doc
