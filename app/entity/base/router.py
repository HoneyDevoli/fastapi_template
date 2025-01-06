from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse

from app.entity.base.deps import get_settings
from app.config.settings import Settings

router = APIRouter(tags=["System"])


@router.get("/health", include_in_schema=False)
async def healthcheck() -> JSONResponse:
    return JSONResponse({}, status_code=status.HTTP_200_OK)


@router.get("/info")
async def get_app_info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.global_.app_name,
        "environment": settings.global_.environment,
        "debug": settings.log.log_level,
    }
