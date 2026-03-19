from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# On définit les modèles de données en utilisant SQLAlchemy ORM
# On définit une classe de base pour tous les modèles, qui hérite de DeclarativeBase
# On ne peut pas hériter directement de DeclarativeBase, il faut créer une classe intermédiaire
class Base(DeclarativeBase):
    pass


class Publisher(Base):
    __tablename__ = "publishers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True)


# En général, on utilise le singulier pour les classes et le pluriel pour les tables
class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    pages: Mapped[int] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    # publisher_id existe en base de données mais il n'y a pas de relationship défini sur Book.
    # Pour accéder à l'éditeur d'un livre, il faut faire une jointure explicite dans la requête.
    publisher_id: Mapped[int | None] = mapped_column(ForeignKey("publishers.id"))
    
    # code ajouté
    
    owner_id: Mapped[int | None] = mapped_column(ForeignKey("persons.id"))
    
    # fin du code ajouté

    author: Mapped[Author] = relationship("Author", back_populates="books")

    book_tags: Mapped[list["BookTag"]] = relationship("BookTag", back_populates="book")


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    book_tags: Mapped[list["BookTag"]] = relationship("BookTag", back_populates="tag")


# Table de jointure entre Book et Tag avec un attribut supplémentaire (date)
# On utilise un modèle explicite plutôt qu'une simple Table pour pouvoir stocker des données
class BookTag(Base):
    __tablename__ = "book_tags"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)
    tagged_at: Mapped[date] = mapped_column()

    book: Mapped["Book"] = relationship("Book", back_populates="book_tags")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="book_tags")
    
## Code ajouter

class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
