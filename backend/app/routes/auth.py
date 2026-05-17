from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import get_settings
from app.auth import create_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    password: str


@router.post("/login")
async def login(body: LoginRequest):
    settings = get_settings()
    if body.password != settings.admin_password:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    token = create_token({"role": "admin"}, settings.token_expire_hours)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/verify")
async def verify_token_route(payload: dict = None):
    from app.auth import require_admin
    from fastapi import Depends
    # Esta ruta se protege en main.py, solo devuelve ok si llega
    return {"ok": True}
