from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.orm import selectinload

from app.db import get_session
from app.models import Author, Book, Publisher, Person
from app.schemas import BookSummary, BookWithAuthor, BookWithAuthorObject, BookWithPublisher, BookWithOwner, PersonOut, PersonWithBooks

router = APIRouter(prefix="/orm", tags=["ORM jointure"])


@router.get("/books-with-authors", response_model=list[BookWithAuthor])
def list_books_with_authors(
    session: Session = Depends(get_session),
) -> list[BookWithAuthor]:
    stmt = (
        select(
            Book.id,
            Book.title,
            Book.pages,
            Author.name.label("author_name"),
        )
        .join(Author)
        .order_by(Book.id)
    )

    # On pourrait aussi utiliser mappings et ** pour éviter de répéter tous les champs de Book :
    # rows = session.execute(stmt).mappings().all()
    # return [BookWithAuthor(**row) for row in rows]

    rows = session.execute(stmt).all()
    return [
        BookWithAuthor(
            id=row.id,
            title=row.title,
            pages=row.pages,
            author_name=row.author_name,
        )
        for row in rows
    ]



@router.get("/books-with-author-object", response_model=list[BookWithAuthorObject])
def list_books_with_author_object(
    session: Session = Depends(get_session),
) -> list[BookWithAuthorObject]:
    # Contrairement à /books-with-authors qui extrait author_name comme simple string,
    # ici on charge des objets Book complets avec book.author navigable (objet Author).
    # joinedload → un seul SELECT avec JOIN, idéal pour une relation many-to-one.
    books = session.scalars(
        select(Book)
        .options(joinedload(Book.author))
        .order_by(Book.id)
    ).all()
    # book.author est un objet Author — on peut accéder à book.author.id, book.author.name
    return books


@router.get("/books-with-publisher", response_model=list[BookWithPublisher])
def list_books_with_publisher(
    session: Session = Depends(get_session),
) -> list[BookWithPublisher]:
    # Publisher n'est pas accessible via book.publisher (pas de relationship défini).
    # On doit donc construire la jointure manuellement avec join() et la condition explicite.
    stmt = (
        select(
            Book.id,
            Book.title,
            Book.pages,
            Publisher.name.label("publisher_name"),
        )
        .join(Publisher, Book.publisher_id == Publisher.id, isouter=True)
        .order_by(Book.id)
    )

    # Idem, on pourrait utiliser mappings et **
    rows = session.execute(stmt).all()
    return [
        BookWithPublisher(
            id=row.id,
            title=row.title,
            pages=row.pages,
            publisher_name=row.publisher_name,
        )
        for row in rows
    ]
    
@router.get("/books-with-owner", response_model=list[BookWithOwner])
def list_books_with_owner(
    session: Session = Depends(get_session),
) -> list[BookWithOwner]:
    stmt = (
        select(
            Book.id,
            Book.title,
            Book.pages,
            Person.id.label("owner_id"),
            Person.first_name.label("owner_first_name"),
            Person.last_name.label("owner_last_name"),
        )
        .join(Person, Book.owner_id == Person.id, isouter=True)
        .order_by(Book.id)
    )

    rows = session.execute(stmt).all()

    return [
        BookWithOwner(
            id=row.id,
            title=row.title,
            pages=row.pages,
            owner=PersonOut(
                id=row.owner_id,
                first_name=row.owner_first_name,
                last_name=row.owner_last_name
            ) if row.owner_id is not None else None
        )
        for row in rows
    ]
    
@router.get("/persons-with-books", response_model=list[PersonWithBooks])
def list_persons_with_books(
    session: Session = Depends(get_session),
) -> list[PersonWithBooks]:
    """
    Retourne tous les Person avec leurs livres (owned_books) en une seule requête.
    Utilise joinedload pour précharger les livres et éviter le N+1 query problem.
    """
    # Charge toutes les personnes avec leurs livres en une seule requête
    persons = session.execute(
        select(Person).options(selectinload(Person.owned_books)).order_by(Person.id)
    ).scalars().all()

    # Retourne la liste au format PersonWithBooks
    return [
        PersonWithBooks(
            id=person.id,
            first_name=person.first_name,
            last_name=person.last_name,
            owned_books=[
                BookSummary(id=book.id, title=book.title)
                for book in person.owned_books
            ]
        )
        for person in persons
    ]
 
