import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlmodel import Session, SQLModel, create_engine, select

from .models import (
    Book, Author, BookCreate, BookPublic, AuthorBookLink, BookWithAuthors
)


load_dotenv()

dbname = os.getenv('POSTGRES_DB')
host = os.getenv('DB_HOST', 'localhost')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
port = os.getenv('DB_PORT')


postgresql_url = f'postgresql://{user}:{password}@{host}/{dbname}'

engine = create_engine(postgresql_url)


def create_db_and_tables():
    """Create engine."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Create session."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


app = FastAPI()


@app.on_event('startup')
def on_startup():
    """Create table on start."""
    create_db_and_tables()


@app.post('/books/', response_model=BookPublic)
async def create_book(book: BookCreate, session: SessionDep):
    """Create book record."""
    db_book = Book(
        title_book=book.title_book,
        price=book.price,
    )

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    for author_input in book.authors:
        stmt = select(Author).where(
            Author.first_name == author_input.first_name,
            Author.second_name == author_input.second_name
        )
        author = session.exec(stmt).first()
        if not author:
            author = Author(
                first_name=author_input.first_name,
                second_name=author_input.second_name
            )
            session.add(author)
            session.commit()
            session.refresh(author)

        link = AuthorBookLink(author_id=author.id, book_id=db_book.id)
        session.add(link)

    session.commit()
    return db_book


@app.get('/books/', response_model=list[BookWithAuthors])
async def get_book(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
):
    """Get all books."""
    books = session.exec(
        select(Book).order_by('adding_date').offset(offset).limit(limit)
    ).all()
    return books


@app.get('/books/{book_id}', response_model=BookPublic)
async def get_one_book(
    book_id: int,
    session: SessionDep,
):
    """Get one book."""
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail='Book not found.')
    return book


@app.patch('/books/{book_id}', response_model=BookCreate)
async def patch_book(
    book_id: int,
    book: BookCreate,
    session: SessionDep,
):
    """Patch book."""
    book_db = session.get(Book, book_id)
    if not book_db:
        raise HTTPException(status_code=404, detail='Book not found.')
    book_data = book.model_dump(exclude_unset=True)
    book_db.sqlmodel_update(book_data)
    session.add(book_db)
    session.commit()
    session.refresh(book_db)

    return book_db


@app.delete('/books/{book_id}')
async def delete_book(book_id: int, session: SessionDep):
    """Delete book."""
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail='Book not found.')
    session.delete(book)
    session.commit()
    return {'Ok': True}
