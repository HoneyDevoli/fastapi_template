import logging
from pathlib import Path

import alembic
import alembic.command
import alembic.config
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.entity.base.db import Base
from app.main import create_application
from app.utils.db import get_db


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return create_application()


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def run_migrations() -> None:
    logging.getLogger('alembic').setLevel(logging.WARNING)
    project_root = Path(__file__).parents[1]
    alembic_ini = project_root / "alembic.ini"
    migrations_path = project_root / "migrations"

    if not alembic_ini.exists() or not migrations_path.is_dir():
        raise FileNotFoundError("Alembic configuration or migrations directory missing.")

    cfg = alembic.config.Config(str(alembic_ini))
    cfg.set_main_option("script_location", str(migrations_path))
    alembic.command.upgrade(cfg, "head")
    yield
    alembic.command.downgrade(cfg, "base")


@pytest.fixture(scope="function", autouse=True)
def clean_database():
    # Удаляем все данные из таблиц
    with get_db() as db_session:
        for table in reversed(Base.metadata.sorted_tables):
            db_session.execute(table.delete())
        db_session.commit()
