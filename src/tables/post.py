from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from .user import User
from .likes import LikesPosts


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=64)
    description: Optional[str] = Field(default=None, max_length=500)
    author_id: int = Field(foreign_key="user.id")
    author: User = Relationship(back_populates="posts")
    liked_users: list[User] = Relationship(back_populates="liked_posts",
                                           link_model=LikesPosts)


def init_posts_table(engine):
    SQLModel.metadata.create_all(engine)
