from typing import Optional

from sqlmodel import SQLModel, Field


class LikesPosts(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    post_id: Optional[int] = Field(
        default=None, foreign_key="post.id", primary_key=True
    )
