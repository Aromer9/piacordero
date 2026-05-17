from pydantic import BaseModel, Field
from typing import Any, Optional
from enum import Enum


class SiteSection(str, Enum):
    hero = "hero"
    about = "about"
    process = "process"
    contact = "contact"
    instagram = "instagram"


class SiteContentUpdate(BaseModel):
    content: dict[str, Any]


class SiteContentOut(BaseModel):
    id: str = Field(alias="_id")
    section: SiteSection
    content: dict[str, Any]

    model_config = {"populate_by_name": True}


def serialize_site_content(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc
