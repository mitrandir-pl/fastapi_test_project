from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound

from tables.user import User
from authentication.auth import Auth
from config.db_settings import engine
from config.error_messages import (
    WRONG_PASSWORD_MESSAGE,
    NO_USER_WITH_EMAIL_MESSAGE,
)


router = APIRouter()


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class LoginHandler:

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.user = None
        self.auth_handler = Auth()

    def user_exists(self):
        with Session(engine) as session:
            statement = select(User).where(User.email == self.email)
            try:
                self.user = session.exec(statement).one()
            except NoResultFound:
                raise HTTPException(status_code=401,
                                    detail=NO_USER_WITH_EMAIL_MESSAGE)
            return self.user

    def check_password(self):
        return self.auth_handler.verify_password(
            self.password, self.user.password
        )

    def get_tokens(self):
        access_token = self.auth_handler.generate_access_token(self.user)
        refresh_token = self.auth_handler.generate_refresh_token(self.user)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }


@router.post("/login")
async def login(user_credentials: UserLoginModel):
    login_handler = LoginHandler(
        user_credentials.email,
        user_credentials.password,
    )
    if login_handler.user_exists():
        if login_handler.check_password():
            return login_handler.get_tokens()
        else:
            raise HTTPException(status_code=401,
                                detail=WRONG_PASSWORD_MESSAGE)
