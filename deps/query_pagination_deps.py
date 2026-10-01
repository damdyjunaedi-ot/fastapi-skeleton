from typing import Annotated, Callable, Generic, Iterator, Type, TypeVar
from fastapi import Depends
from fastapi_pagination import Params

T = TypeVar("T")


class DefaultParams(Params):
    page: int = 1
    size: int = 50


class QueryParams(Generic[T]):
    def __init__(self, filters: T, pagination: Params):
        self.filters = filters
        self.pagination = pagination

    def __iter__(self) -> Iterator:
        yield self.filters
        yield self.pagination


def query_with_pagination(schema: Type[T]) -> Callable[..., QueryParams[T]]:
    async def dependency(
        filters: Annotated[T, Depends(schema)],
        pagination: DefaultParams = Depends(),
    ) -> QueryParams[T]:
        return QueryParams(
            filters=filters,
            pagination=pagination,
        )

    return dependency
