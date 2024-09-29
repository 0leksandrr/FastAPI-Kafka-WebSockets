from typing import (
    Generic,
    TypeVar,
)

from pydantic import BaseModel


class ErrorSchema(BaseModel):
    error: str


R = TypeVar('R')


class BaseQueryResponseSchema(BaseModel, Generic[R]):
    count: int
    offset: int
    limit: int
    items: R
