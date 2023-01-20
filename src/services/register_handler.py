from fastapi import HTTPException
from pydantic import BaseModel, Field, EmailStr
from sqlmodel import Session, select

from tables.user import User
from config.db_settings import engine
from config.error_messages import (
    USER_WITH_THIS_EMAIL_ALREADY_EXISTS,
    USER_WITH_THIS_USERNAME_ALREADY_EXISTS,
)


class UserModelRegister(BaseModel):
    email: EmailStr
    username: str | None = None
    password: str = Field(min_length=8)


class RegisterHandler:

    def __init__(self, email: str, username: str, password: str):
        self.email = email
        self.username = username
        self.password = password

    def check_email(self, session: Session) -> bool:
        """Method checks if user with this email already exists"""
        statement = select(User).where(User.email == self.email)
        if session.exec(statement).first():
            raise HTTPException(
                status_code=401,
                detail=USER_WITH_THIS_EMAIL_ALREADY_EXISTS)
        else:
            return True

    def check_username(self, session: Session) -> bool:
        """Method checks if user with this username already exists"""
        statement = select(User).where(User.username == self.username)
        if session.exec(statement).first():
            raise HTTPException(
                status_code=401,
                detail=USER_WITH_THIS_USERNAME_ALREADY_EXISTS)
        else:
            return True

    def user_not_exists(self, session: Session) -> bool:
        """Method checks if user with such email and username don't exists"""
        return self.check_email(session) and self.check_username(session)

    def create_user(self) -> User:
        """Method creates a new user"""
        return User(
            username=self.username,
            email=self.email,
            password=self.password,
        )
