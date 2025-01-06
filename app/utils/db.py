import logging
from contextlib import contextmanager
from typing import Generator

from psycopg import OperationalError
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from tenacity import retry, stop_after_attempt, wait_fixed

from app.config.settings import settings

logger = logging.getLogger(__name__)

MAX_TRIES = 3  # секунды
WAIT_SECONDS = 1
engine = create_engine(settings.db.url,
                       echo=settings.db.echo,
                       echo_pool=settings.db.echo_pool)
SessionBuilder = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@retry(
    stop=stop_after_attempt(MAX_TRIES),
    wait=wait_fixed(WAIT_SECONDS),
)
def check_database_connection():
    logger.info("Checking database connection")
    try:
        _execute_db_query()
        logger.info("Database connection successful")
    except OperationalError as e:
        logger.info(f"Database connection failed: {e}")
        raise


def _execute_db_query():
    with get_db() as conn:
        query_result = conn.execute(text("SELECT 1"))
        query_result = query_result.cursor.fetchone()
        if query_result is None or query_result[0] != 1:
            raise ValueError("Unexpected result from database")


@contextmanager
def get_db() -> Generator[Session, None, None]:
    db_session = SessionBuilder()
    try:
        yield db_session
    finally:
        db_session.close()
