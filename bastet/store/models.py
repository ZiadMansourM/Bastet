from sqlmodel import SQLModel, Field
from typing import Optional


# --------------------> Base Schema "CRUD"
class BookBase(SQLModel):
    title: str
    description: str


# --------------------> DB Schema
class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


# --------------------> Create Schema "C"
class BookCreate(BookBase):
    pass


# --------------------> List Schema "R"
class BookRead(BookBase):
    id: int


# --------------------> Update Schema "U"
class BookUpdate(BookBase):
    title: Optional[str] = None
    description: Optional[str] = None