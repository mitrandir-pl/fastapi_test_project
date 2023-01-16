from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr

from .likes import LikesPosts


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str | None = Field(default=None, unique=True)
    email: EmailStr = Field(unique=True)
    password: str = Field(min_length=8, max_length=64)
    posts: Optional[list["Post"]] = Relationship(back_populates="author")
    liked_posts: list["Post"] = Relationship(back_populates="liked_users",
                                             link_model=LikesPosts)


def init_users_table(engine):
    SQLModel.metadata.create_all(engine)
