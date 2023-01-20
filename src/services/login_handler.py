from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound

from tables.user import User
from authentication.auth import Auth
from config.error_messages import NO_USER_WITH_EMAIL_MESSAGE


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class LoginHandler:

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.user = None
        self.auth_handler = Auth()

    def user_exists(self, session: Session) -> User:
        """Method checks if such user already exists"""
        statement = select(User).where(User.email == self.email)
        try:
            self.user = session.exec(statement).one()
        except NoResultFound:
            raise HTTPException(status_code=401,
                                detail=NO_USER_WITH_EMAIL_MESSAGE)
        return self.user

    def check_password(self) -> bool:
        """Method checks the password"""
        return self.auth_handler.verify_password(
            self.password, self.user.password
        )

    def get_tokens(self) -> dict[str: str]:
        """Method generates and returns tokens by user id"""
        access_token = self.auth_handler.generate_access_token(self.user.id)
        refresh_token = self.auth_handler.generate_refresh_token(self.user.id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
