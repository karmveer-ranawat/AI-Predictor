# backend/route/auth_routes.py
from fastapi import APIRouter, HTTPException, Request
from kite_auth.kite_session import get_kite, save_token, login_and_cache
from pydantic import BaseModel
import os

router = APIRouter()

class TokenRequest(BaseModel):
    request_token: str

@router.get("/login_url")
def get_login_url():
    try:
        kite = get_kite(allow_cli_fallback=False)
        return {"login_url": kite.login_url()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/token")
def exchange_token(data: TokenRequest):
    try:
        kite = get_kite(allow_cli_fallback=False)
        session = kite.generate_session(data.request_token, os.getenv("API_SECRET"))
        kite.set_access_token(session["access_token"])
        save_token(session)
        return {"access_token": session["access_token"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/profile")
def get_profile():
    try:
        kite = get_kite(allow_cli_fallback=False)
        profile = kite.profile()
        return profile
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
