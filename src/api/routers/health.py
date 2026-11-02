from fastapi import APIRouter
from fastapi.responses import JSONResponse

from api.database import fetch_one

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def get_health():
    return {"status": "ok"}


@router.get("/ready")
def get_readyness():
    try:
        fetch_one("select 1 as ok")
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"status": "error", "database": "unavailable"},
        )
    return {"status": "ok", "database": "ok"}
