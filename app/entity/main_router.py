from fastapi import APIRouter

import app.entity.base.router as system
import app.entity.order.v1.router as order
from app.config.settings import settings

main_router = APIRouter()
main_router.include_router(order.router)

if settings.is_dev:
    main_router.include_router(system.router)
