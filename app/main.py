from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from httpx import HTTPError
from sqlalchemy.exc import IntegrityError, ProgrammingError, NoResultFound
from starlette.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.entity.main_router import main_router
from app.config import exception_config as exh
from app.config.log_config import config_logging_dev, config_logging_prod
from app.config.settings import Environment, settings
from app.utils import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = settings
    if settings.global_.environment == Environment.prod:
        config_logging_prod()
    else:
        config_logging_dev()

    db.check_database_connection()
    yield
    # То что будет выполнено после завершения работы приложения


def custom_exception_handler(app: FastAPI):
    app.add_exception_handler(RequestValidationError, exh.req_validation_handler)
    app.add_exception_handler(ValidationError, exh.validation_handler)
    app.add_exception_handler(AttributeError, exh.attribute_error_handler)

    app.add_exception_handler(NoResultFound, exh.data_not_found_error_handler)
    app.add_exception_handler(IntegrityError, exh.sql_error_handler)
    app.add_exception_handler(ProgrammingError, exh.sql_error_handler)
    app.add_exception_handler(HTTPError, exh.http_error_handler)
    app.add_exception_handler(HTTPException, exh.http_exception_handler)


def create_application() -> FastAPI:
    application = FastAPI(
        title="Template FastAPI",
        debug=settings.is_dev,
        lifespan=lifespan,
    )

    if settings.global_.environment == Environment.prod:
        application.openapi_url = None

    custom_exception_handler(application)
    application.include_router(main_router)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:create_application",
        factory=True,
        host=settings.global_.host,
        port=settings.global_.port,
        log_level=settings.log.log_level,
        access_log=True,
        reload=settings.is_dev,
    )
