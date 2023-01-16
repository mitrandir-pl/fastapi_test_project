from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr

from config.db_settings import engine
from tables.user import User
from tables.post import Post


class UserListOutModel(BaseModel):
    id_: int
    username: str
    email: EmailStr


class UserOutModel(UserListOutModel):
    posts: list[Post] | None = None


class UsersHandler:

    def get_users_list(self) -> list[UserListOutModel]:
        """Method returns list of users"""
        statement = select(User)
        with Session(engine) as session:
            user_list = list()
            for user in session.exec(statement).all():
                user_list.append(UserListOutModel(
                    id_=user.id,
                    username=user.username,
                    email=user.email,
                ))
            return user_list

    def get_user_by_id(self, user_id: int) -> UserOutModel:
        """Method returns user by id"""
        with Session(engine) as session:
            user = session.get(User, user_id)
            return UserOutModel(
                id_=user.id,
                username=user.username,
                email=user.email,
                posts=user.posts,
            )
