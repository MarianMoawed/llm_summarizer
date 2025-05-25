from fastapi import FastAPI,APIRouter, Depends
from helpers.config import get_settings, Settings


base_router = APIRouter(prefix="/api/v1", tags=["base"])

settings= get_settings()

@base_router.get("/")
def read_root(settings:Settings=Depends(get_settings)):
    
    app_name = settings.APP_NAME
    app_version = settings.APP_VERSION

    return {
        "app_name": app_name,
        "app_version": app_version,
    }