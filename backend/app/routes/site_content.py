from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from app.config import get_db
from app.auth import require_admin
from app.models.site_content import (
    SiteContentUpdate,
    SiteSection,
    serialize_site_content,
)

router = APIRouter(prefix="/api/site-content", tags=["site-content"])


@router.get("")
async def get_all_content():
    db = get_db()
    result = {}
    async for doc in db.site_content.find():
        result[doc["section"]] = serialize_site_content(doc)
    return result


@router.get("/{section}")
async def get_section_content(section: SiteSection):
    db = get_db()
    doc = await db.site_content.find_one({"section": section.value})
    if not doc:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    return serialize_site_content(doc)


@router.put("/{section}", dependencies=[Depends(require_admin)])
async def update_section_content(section: SiteSection, data: SiteContentUpdate):
    db = get_db()
    result = await db.site_content.update_one(
        {"section": section.value},
        {"$set": {"content": data.content}},
        upsert=True,
    )
    doc = await db.site_content.find_one({"section": section.value})
    return serialize_site_content(doc)
