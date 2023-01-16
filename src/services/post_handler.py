from fastapi import HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel, Field

from tables.post import Post
from tables.user import User
from config.db_settings import engine
from authentication.auth import Auth
from config.error_messages import (
    STRANGER_POST_UPDATE_MESSAGE,
    STRANGER_POST_DELETE_MESSAGE,
    LIKE_SET_MESSAGE,
    LIKE_REMOVED_MESSAGE,
)


class PostModel(BaseModel):
    title: str = Field(max_length=64)
    description: str | None = Field(default=None, max_length=500)


class PostsHandler:

    def __init__(self):
        self.auth_handler = Auth()

    def get_posts_list(self) -> list[Post]:
        """Method returns list of all posts"""
        statement = select(Post)
        with Session(engine) as session:
            return session.exec(statement).all()

    def get_post_by_id(self, post_id: int) -> Post:
        """Method returns post by current id"""
        with Session(engine) as session:
            return session.get(Post, post_id)

    def create_post(self, post: PostModel, token: str) -> None:
        """Method creates a post"""
        payload = self.auth_handler.decode_token(token)
        with Session(engine) as session:
            user = session.get(User, payload["user_id"])
            created_post = Post(
                title=post.title,
                description=post.description,
                author_id=user.id,
                author=user,
            )
            session.add(created_post)
            session.commit()

    def update_post(self, updated_post: PostModel, post_id: int, token: str) -> None:
        """Method updates a post"""
        payload = self.auth_handler.decode_token(token)
        with Session(engine) as session:
            user = session.get(User, payload["user_id"])
            post = session.get(Post, post_id)
            if post.author == user:
                for key, value in updated_post.dict():
                    setattr(post, key, value)
                session.add(post)
                session.commit()
            else:
                raise HTTPException(status_code=400,
                                    detail=STRANGER_POST_UPDATE_MESSAGE)

    def delete_post(self, post_id: int, token: str) -> None:
        """Method deletes a post"""
        payload = self.auth_handler.decode_token(token)
        with Session(engine) as session:
            user = session.get(User, payload["user_id"])
            post = session.get(Post, post_id)
            if post.author == user:
                session.delete(post)
                session.commit()
            else:
                raise HTTPException(status_code=400,
                                    detail=STRANGER_POST_DELETE_MESSAGE)

    def set_like(self, post_id: int, token: str) -> str:
        """Method sets like. If it's already set, method removes it"""
        payload = self.auth_handler.decode_token(token)
        with Session(engine) as session:
            user = session.get(User, payload["user_id"])
            post = session.get(Post, post_id)
            if user not in post.liked_users:
                post.liked_users.append(user)
                session.add(post)
                session.commit()
                return LIKE_SET_MESSAGE
            else:
                post.liked_users.remove(user)
                session.add(post)
                session.commit()
                return LIKE_REMOVED_MESSAGE
