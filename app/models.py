from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship


MAX_LENGTH_NAME = 20
MAX_LENGTH_TITLE = 50


class AuthorBookLink(SQLModel, table=True):
    """Link Model for authors and books."""

    author_id: int | None = Field(
        default=None,
        foreign_key='author.id',
        primary_key=True
    )
    book_id: int | None = Field(
        default=None,
        foreign_key='book.id',
        primary_key=True
    )


class AuthorBase(SQLModel):
    """Base model for author."""

    first_name: str = Field(max_length=MAX_LENGTH_NAME)
    second_name: str = Field(index=True, max_length=MAX_LENGTH_NAME)


class Author(AuthorBase, table=True):
    """Model for authors."""

    id: int | None = Field(default=None, primary_key=True)
    books: list['Book'] = Relationship(
        back_populates='authors',
        link_model=AuthorBookLink
    )


class BookBase(SQLModel):
    """Base model for book."""

    title_book: str = Field(index=True, max_length=MAX_LENGTH_TITLE)
    price: Optional[float] = Field(default=0, gt=-1)


class Book(BookBase, table=True):
    """Model for books."""

    id: int | None = Field(default=None, primary_key=True)
    adding_date: datetime = Field(
        default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    authors: list['Author'] = Relationship(
        back_populates='books',
        link_model=AuthorBookLink
    )


class AuthorInput(SQLModel):
    """Representation for names of authors."""

    first_name: str
    second_name: str


class BookPublic(BookBase):
    """Public model for book."""

    id: int
    authors: list[AuthorInput]


class AuthorPublic(SQLModel):
    """Representation for authors."""

    first_name: str
    second_name: str


class BookWithAuthors(BookBase):
    """Public model for authors."""

    adding_date: datetime
    id: int
    authors: list[AuthorPublic]


class BookCreate(BookBase):
    """Model to create book."""

    authors: list[AuthorInput]
