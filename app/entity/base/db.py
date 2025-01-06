from datetime import UTC, datetime

import sqlalchemy as sa
from sqlalchemy import BigInteger, Column, DateTime, MetaData
from sqlalchemy.orm import declarative_base

"""
alembic requires constraints to be named.
This sets up a naming convention rather than manually naming
https://alembic.sqlalchemy.org/en/latest/naming.html
"""
POSTGRES_INDEXES_NAMING_CONVENTION = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}
meta = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)
Base = declarative_base(metadata=meta)  # ORM base class


class BaseOrm(Base):
    """
    Provides primary key column, created and updated timestamps
    """

    __abstract__ = True
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        onupdate=datetime.now(UTC),
        server_default=sa.text('CURRENT_TIMESTAMP'),
    )
