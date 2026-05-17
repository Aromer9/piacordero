from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.config import get_settings
from app.routes import products, site_content, upload, auth

settings = get_settings()

app = FastAPI(
    title="Pía Cordero Pastelería API",
    version="1.0.0",
    description="API para el sitio web de Pía Cordero Pastelería artesanal",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(site_content.router)
app.include_router(upload.router)


@app.get("/api/config")
async def public_config(request: Request):
    """Origen público del backend para armar URLs de /uploads en el front (sin depender solo de VITE en build)."""
    explicit = (settings.public_base_url or "").strip().rstrip("/")
    if explicit:
        return {"media_origin": explicit}
    host = (request.headers.get("x-forwarded-host") or request.headers.get("host") or "").split(",")[0].strip()
    proto = (request.headers.get("x-forwarded-proto") or "http").split(",")[0].strip()
    if not host:
        return {"media_origin": ""}
    return {"media_origin": f"{proto}://{host}".rstrip("/")}


upload_dir = Path(settings.upload_dir)
upload_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")


@app.get("/")
async def root():
    return {"message": "Pía Cordero Pastelería API", "status": "ok"}


@app.get("/health")
async def health():
    return {"status": "ok"}
