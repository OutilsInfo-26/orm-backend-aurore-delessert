import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@db:5432/orm_demo",
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    from datetime import date

    from app.models import Base, Author, Book, Tag, BookTag, Publisher, Person
    from sqlalchemy import func, select

    Base.metadata.create_all(bind=engine) # Create tables if they don't exist

    with SessionLocal() as session:
        author_count = session.scalar(select(func.count(Author.id)))
        if author_count:
            return

        publishers = [
            Publisher(name="Gallimard"),          # 0
            Publisher(name="Addison-Wesley"),      # 1
            Publisher(name="Allen & Unwin"),       # 2
            Publisher(name="Cambridge UP"),        # 3
        ]
        session.add_all(publishers)
        session.flush()

        authors = [
            # Informatique
            Author(name="Ada Lovelace"),        # 0
            Author(name="Grace Hopper"),         # 1
            Author(name="Alan Turing"),          # 2
            Author(name="Donald Knuth"),         # 3
            Author(name="Linus Torvalds"),       # 4
            # Littérature classique
            Author(name="Marcel Proust"),        # 5
            Author(name="J.R.R. Tolkien"),       # 6
            Author(name="Victor Hugo"),          # 7
            Author(name="Albert Camus"),         # 8
        ]
        session.add_all(authors)
        session.flush()
        
        persons = [
            Person(first_name="Aurore", last_name="Delessert"),
            Person(first_name="Ophélie", last_name="Jacot"),
            Person(first_name="David", last_name="Guisolan"),
            Person(first_name="Florian", last_name="Sommerhalder"),
        ]
        session.add_all(persons)
        session.flush()

        books = [
            # Informatique
            Book(title="Notes on the Analytical Engine", pages=120, author_id=authors[0].id, publisher_id=publishers[3].id, owner_id=persons[0].id),
            Book(title="Compilers and Cobol", pages=220, author_id=authors[1].id, publisher_id=publishers[1].id, owner_id=persons[1].id),
            Book(title="Computing Machinery and Intelligence", pages=90, author_id=authors[2].id, publisher_id=publishers[3].id, owner_id=persons[2].id),
            Book(title="The Art of Computer Programming Vol. 1", pages=672, author_id=authors[3].id, publisher_id=publishers[1].id, owner_id=persons[3].id),
            Book(title="The Art of Computer Programming Vol. 2", pages=784, author_id=authors[3].id, publisher_id=publishers[1].id, owner_id=persons[0].id),
            Book(title="Just for Fun", pages=280, author_id=authors[4].id, owner_id=persons[3].id),
            # Proust — À la recherche du temps perdu
            Book(title="Du côté de chez Swann", pages=531, author_id=authors[5].id, publisher_id=publishers[0].id, owner_id=None),
            Book(title="À l'ombre des jeunes filles en fleurs", pages=619, author_id=authors[5].id, publisher_id=publishers[0].id, owner_id=persons[1].id),
            Book(title="Le Temps retrouvé", pages=524, author_id=authors[5].id, publisher_id=publishers[0].id, owner_id=None),
            # Tolkien
            Book(title="The Fellowship of the Ring", pages=423, author_id=authors[6].id, publisher_id=publishers[2].id, owner_id=persons[3].id),
            Book(title="The Two Towers", pages=352, author_id=authors[6].id, publisher_id=publishers[2].id, owner_id=persons[3].id),
            Book(title="The Return of the King", pages=416, author_id=authors[6].id, publisher_id=publishers[2].id, owner_id=persons[3].id),
            # Autres classiques
            Book(title="Les Misérables", pages=1900, author_id=authors[7].id, publisher_id=publishers[0].id, owner_id=persons[0].id),
            Book(title="L'Étranger", pages=186, author_id=authors[8].id, publisher_id=publishers[0].id, owner_id=None),
        ]
        session.add_all(books)
        session.flush()

        tags = [
            Tag(name="algorithms"),         # 0
            Tag(name="history"),            # 1
            Tag(name="ai"),                 # 2
            Tag(name="compilers"),          # 3
            Tag(name="operating-systems"),  # 4
            Tag(name="mathematics"),        # 5
            Tag(name="classic"),            # 6
            Tag(name="fantasy"),            # 7
            Tag(name="fiction"),            # 8
            Tag(name="french-literature"),  # 9
        ]
        session.add_all(tags)
        session.flush()

        book_tags = [
            # Informatique
            BookTag(book_id=books[0].id, tag_id=tags[1].id, tagged_at=date(2024, 1, 10)),
            BookTag(book_id=books[0].id, tag_id=tags[5].id, tagged_at=date(2024, 1, 10)),
            BookTag(book_id=books[1].id, tag_id=tags[3].id, tagged_at=date(2024, 2, 15)),
            BookTag(book_id=books[2].id, tag_id=tags[2].id, tagged_at=date(2024, 3, 5)),
            BookTag(book_id=books[2].id, tag_id=tags[1].id, tagged_at=date(2024, 3, 5)),
            BookTag(book_id=books[3].id, tag_id=tags[0].id, tagged_at=date(2024, 4, 20)),
            BookTag(book_id=books[3].id, tag_id=tags[5].id, tagged_at=date(2024, 4, 20)),
            BookTag(book_id=books[4].id, tag_id=tags[0].id, tagged_at=date(2024, 4, 21)),
            BookTag(book_id=books[5].id, tag_id=tags[4].id, tagged_at=date(2024, 5, 1)),
            BookTag(book_id=books[5].id, tag_id=tags[1].id, tagged_at=date(2024, 5, 1)),
            # Proust
            BookTag(book_id=books[6].id, tag_id=tags[6].id, tagged_at=date(2024, 6, 1)),
            BookTag(book_id=books[6].id, tag_id=tags[9].id, tagged_at=date(2024, 6, 1)),
            BookTag(book_id=books[6].id, tag_id=tags[8].id, tagged_at=date(2024, 6, 1)),
            BookTag(book_id=books[7].id, tag_id=tags[6].id, tagged_at=date(2024, 6, 2)),
            BookTag(book_id=books[7].id, tag_id=tags[9].id, tagged_at=date(2024, 6, 2)),
            BookTag(book_id=books[8].id, tag_id=tags[6].id, tagged_at=date(2024, 6, 3)),
            BookTag(book_id=books[8].id, tag_id=tags[9].id, tagged_at=date(2024, 6, 3)),
            # Tolkien
            BookTag(book_id=books[9].id,  tag_id=tags[7].id, tagged_at=date(2024, 7, 10)),
            BookTag(book_id=books[9].id,  tag_id=tags[8].id, tagged_at=date(2024, 7, 10)),
            BookTag(book_id=books[10].id, tag_id=tags[7].id, tagged_at=date(2024, 7, 11)),
            BookTag(book_id=books[10].id, tag_id=tags[8].id, tagged_at=date(2024, 7, 11)),
            BookTag(book_id=books[11].id, tag_id=tags[7].id, tagged_at=date(2024, 7, 12)),
            BookTag(book_id=books[11].id, tag_id=tags[8].id, tagged_at=date(2024, 7, 12)),
            # Autres classiques
            BookTag(book_id=books[12].id, tag_id=tags[6].id, tagged_at=date(2024, 8, 1)),
            BookTag(book_id=books[12].id, tag_id=tags[9].id, tagged_at=date(2024, 8, 1)),
            BookTag(book_id=books[13].id, tag_id=tags[6].id, tagged_at=date(2024, 8, 5)),
            BookTag(book_id=books[13].id, tag_id=tags[9].id, tagged_at=date(2024, 8, 5)),
            BookTag(book_id=books[13].id, tag_id=tags[8].id, tagged_at=date(2024, 8, 5)),
        ]
        session.add_all(book_tags)
        session.commit()
