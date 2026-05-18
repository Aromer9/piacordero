import io
import uuid
from pathlib import Path

import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, File, HTTPException, UploadFile
import aiofiles

from app.config import get_settings

router = APIRouter(prefix="/api/upload", tags=["upload"])

IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif", "image/avif"}
VIDEO_TYPES = {"video/mp4", "video/webm", "video/quicktime", "video/x-m4v"}
ALLOWED_TYPES = IMAGE_TYPES | VIDEO_TYPES

IMAGE_MAX_BYTES = 8 * 1024 * 1024   # 8 MB
VIDEO_MAX_BYTES = 80 * 1024 * 1024  # 80 MB

DEFAULT_EXTS = {
    "image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp",
    "image/gif": ".gif", "image/avif": ".avif",
    "video/mp4": ".mp4", "video/webm": ".webm",
    "video/quicktime": ".mov", "video/x-m4v": ".m4v",
}


def _configure_cloudinary(settings) -> None:
    cloudinary.config(
        cloud_name=settings.cloudinary_cloud_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )


async def _upload_to_cloudinary(content: bytes, content_type: str) -> str:
    """Sube bytes a Cloudinary y devuelve la URL pública (HTTPS, CDN)."""
    is_video = content_type in VIDEO_TYPES
    resource_type = "video" if is_video else "image"
    result = cloudinary.uploader.upload(
        io.BytesIO(content),
        folder="piacordero",
        resource_type=resource_type,
        overwrite=False,
    )
    return result["secure_url"]


async def _upload_to_disk(content: bytes, content_type: str, settings) -> str:
    """Fallback: guarda en disco local (solo dev; se pierde en cada deploy)."""
    raw_ext = DEFAULT_EXTS.get(content_type, ".bin")
    filename = f"{uuid.uuid4().hex}{raw_ext}"
    upload_path = Path(settings.upload_dir) / filename
    upload_path.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(upload_path, "wb") as f:
        await f.write(content)
    return f"/uploads/{filename}"


@router.post("")
async def upload_media(file: UploadFile = File(...)):
    settings = get_settings()
    content_type = (file.content_type or "").split(";")[0].strip().lower()

    if content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Tipo de archivo no permitido. Use JPEG, PNG, WebP, GIF (imagen) o MP4, WebM, MOV (vídeo).",
        )

    is_video = content_type in VIDEO_TYPES
    max_bytes = VIDEO_MAX_BYTES if is_video else IMAGE_MAX_BYTES

    content = await file.read()
    if len(content) > max_bytes:
        limit_mb = max_bytes // (1024 * 1024)
        raise HTTPException(
            status_code=413,
            detail=f"Archivo demasiado grande. Límite: {limit_mb} MB.",
        )

    if settings.cloudinary_enabled:
        _configure_cloudinary(settings)
        try:
            url = await _upload_to_cloudinary(content, content_type)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al subir a Cloudinary: {e}")
    else:
        url = await _upload_to_disk(content, content_type, settings)

    return {
        "url": url,
        "media_type": "video" if is_video else "image",
    }
