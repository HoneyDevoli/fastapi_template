from math import ceil
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Query


class PageRequestSchema(BaseModel):
    page: int | None = 1
    size: int | None = 25
    sort: str | None = 'created_at'
    order: Literal['ASC', 'DESC'] | None = 'DESC'

    @property
    def offset(self):
        return (self.page - 1) * self.size

    def build(self, query: Query, sort):
        sort = sort.asc() if self.order == 'ASC' else sort.desc()
        return query.order_by(sort).limit(self.size).offset(self.offset)


ResponseDataType = TypeVar('ResponseDataType')


class PageResponseSchema(BaseModel, Generic[ResponseDataType]):
    data: list[ResponseDataType]
    total_count: int
    page_size: int
    total_pages: int | None = None

    @field_validator('page_size')
    def validate_page_size(cls, value: int) -> int:
        if value <= 0:
            raise ValueError('page_size must be greater than 0')
        return value

    @field_validator('total_pages', mode='after')  # Ensure it runs after other validators.
    def calculate_pages(cls, value: int | None, values: dict) -> int:
        # Safely grab validated fields from 'values'
        total_count = values.get('total_count', 0)
        page_size = values.get('page_size')

        # Check for invalid page_size
        if page_size is None or page_size <= 0:
            raise ValueError('page_size must be a positive integer.')

        return ceil(total_count / page_size) if total_count > 0 else 1
