from datetime import date

from pydantic import BaseModel, Field


class AuthorCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Author full name")

    model_config = {
        "json_schema_extra": {
            "example": {"name": "Ada Lovelace"}
        }
    }


class AuthorUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)


class AuthorOut(AuthorCreate):
    id: int

    model_config = {
        "from_attributes": True,
    }


class BookCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=200, description="Book title")
    pages: int = Field(..., gt=0, le=2000, description="Number of pages")
    author_id: int = Field(..., gt=0, description="Existing author id")
    owner_id: int | None = Field(None, gt=0, description="Existing person id")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Notes on the Analytical Engine",
                "pages": 120,
                "author_id": 1,
                "owner_id": 1,
            }
        }
    }


class BookOut(BookCreate):
    id: int

    model_config = {
        "from_attributes": True,
    }


class BookSummary(BaseModel):
    id: int
    title: str


class BookWithAuthor(BaseModel):
    id: int
    title: str
    pages: int
    author_name: str


# Contrairement à BookWithAuthor, ici author est un objet imbriqué
# accessible via la navigation ORM (book.author.id, book.author.name)
class BookWithAuthorObject(BaseModel):
    id: int
    title: str
    pages: int
    author: AuthorOut

    model_config = {"from_attributes": True}


class BookWithPublisher(BaseModel):
    id: int
    title: str
    pages: int
    publisher_name: str | None


class TagOut(BaseModel):
    name: str
    tagged_at: date

    model_config = {"from_attributes": True}


class BookWithTags(BaseModel):
    id: int
    title: str
    tags: list[TagOut]

    model_config = {"from_attributes": True}

# Code ajouté

class PersonOut(BaseModel):
    id: int
    first_name: str
    last_name: str

    model_config = {"from_attributes": True}
    
class BookWithOwner(BaseModel):
    id: int
    title: str
    owner: PersonOut | None

    model_config = {"from_attributes": True}
    
class PersonCreate(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=100, description="Person first name")
    last_name: str = Field(..., min_length=2, max_length=100, description="Person last name")

    model_config = {
        "json_schema_extra": {
            "example": {"first_name": "Alice", "last_name": "Smith"}
        }
    }
    
class BookWithOwner(BaseModel):
    id: int
    title: str
    owner: PersonOut | None

    model_config = {"from_attributes": True}

# fin du code ajouté