from typing import TypedDict, Optional


class TWatchData(TypedDict):
    jwt: str
    ip: str


class TPagination(TypedDict):
    current_page: int
    total_pages: int
    total_entries: int
    per_page: int


class ResponsePagination(TypedDict):
    items: list[object]
    pagination: TPagination
