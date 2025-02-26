from enum import StrEnum

from fastapi import Query
from pydantic import BaseModel


class SortEnum(StrEnum):
    ASC = "asc"
    DESC = "desc"


class Pagination(BaseModel):
    perPage: int
    page: int
    order: SortEnum


def pagination_params(
    page: int = Query(
        ge=1,
        le=5000,
        required=False,
        default=1,
        description="Number of page",
    ),
    perPage: int = Query(
        ge=1,
        le=100,
        required=False,
        default=10,
        description="Count elements on page",
    ),
    order: SortEnum = Query(
        default=SortEnum.DESC,
        description="Sorting by time",
    ),
) -> Pagination:
    return Pagination(perPage=perPage, page=page, order=order)
