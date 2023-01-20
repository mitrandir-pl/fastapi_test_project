from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr

from tables.user import User
from tables.post import Post


class UserListOutModel(BaseModel):
    id_: int
    username: str
    email: EmailStr


class UserOutModel(UserListOutModel):
    posts: list[Post] | None = None


class UsersHandler:

    def get_users_list(self, session: Session) -> list[UserListOutModel]:
        """Method returns list of users"""
        statement = select(User)
        user_list = list()
        for user in session.exec(statement).all():
            user_list.append(UserListOutModel(
                id_=user.id,
                username=user.username,
                email=user.email,
            ))
        return user_list

    def get_user_by_id(self, user_id: int, session: Session) -> UserOutModel:
        """Method returns user by id"""
        user = session.get(User, user_id)
        return UserOutModel(
            id_=user.id,
            username=user.username,
            email=user.email,
            posts=user.posts,
        )
