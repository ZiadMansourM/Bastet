from fastapi import APIRouter, status, Response, Depends
from fastapi.exceptions import HTTPException
from sqlmodel import select, Session
import models
from bastet.conf.database import get_session


router = APIRouter(
    prefix="/books",
    tags=["store"],
)


# ----------------> Book List
@router.get('/',
    response_model=list[models.BookRead],
    status_code=status.HTTP_200_OK
)
async def list_books(session: Session = Depends(get_session)):
    return session.exec(select(models.Book)).all()


# ----------------> Book Detail
@router.get('/{book_id}',
    response_model=models.BookRead,
    status_code=status.HTTP_200_OK
)
async def get_book(
        book_id: int, 
        session: Session = Depends(get_session)
    ):
    book = session.get(models.Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book


# ----------------> Book Create
@router.post('/',
    response_model=models.BookRead,
    status_code=status.HTTP_201_CREATED
)
async def create_book(
        book: models.BookCreate, 
        session: Session = Depends(get_session)
    ):
    new_book = models.Book(title=book.title, description=book.description)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book


# ----------------> Book Update
@router.put('/{book_id}', 
    response_model=models.BookRead,
    status_code=status.HTTP_202_ACCEPTED
)
async def update_book(
        book_id: int, 
        book: models.BookUpdate, 
        session: Session = Depends(get_session)
    ):
    db_book = session.get(models.Book, book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    book_data = book.dict(exclude_unset=True)
    for key, value in book_data.items():
        setattr(db_book, key, value)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


# ----------------> Book Delete
@router.delete('/{book_id}',
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book(
        book_id: int, 
        session: Session = Depends(get_session)
    ):
    db_book = session.get(models.Book, book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book Not Found"
        )
    session.delete(db_book)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)