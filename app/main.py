from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from httpx import HTTPError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound, ProgrammingError
from starlette.exceptions import HTTPException

from app.config import exception_config as exh
from app.config.settings import Environment, settings
from app.entity.main_router import main_router
from app.utils import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = settings

    db.check_database_connection()

    yield


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
        title='Template FastAPI',
        debug=settings.is_dev,
        lifespan=lifespan,
    )

    if settings.global_.environment == Environment.prod:
        application.openapi_url = None

    custom_exception_handler(application)
    application.include_router(main_router)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    return application
