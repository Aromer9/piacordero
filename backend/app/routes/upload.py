from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import aiofiles
import uuid

from app.config import get_settings

router = APIRouter(prefix="/api/upload", tags=["upload"])

IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif", "image/avif"}
VIDEO_TYPES = {"video/mp4", "video/webm", "video/quicktime", "video/x-m4v"}
ALLOWED_TYPES = IMAGE_TYPES | VIDEO_TYPES

# 8 MB para imágenes, 80 MB para vídeos
IMAGE_MAX_BYTES = 8 * 1024 * 1024
VIDEO_MAX_BYTES = 80 * 1024 * 1024

DEFAULT_EXTS = {
    "image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp",
    "image/gif": ".gif", "image/avif": ".avif",
    "video/mp4": ".mp4", "video/webm": ".webm",
    "video/quicktime": ".mov", "video/x-m4v": ".m4v",
}


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

    raw_ext = Path(file.filename or "").suffix.lower()
    ext = raw_ext if raw_ext in {v for v in DEFAULT_EXTS.values()} else DEFAULT_EXTS.get(content_type, ".bin")
    filename = f"{uuid.uuid4().hex}{ext}"
    upload_path = Path(settings.upload_dir) / filename
    upload_path.parent.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(upload_path, "wb") as f:
        await f.write(content)

    return {
        "url": f"/uploads/{filename}",
        "filename": filename,
        "media_type": "video" if is_video else "image",
    }
