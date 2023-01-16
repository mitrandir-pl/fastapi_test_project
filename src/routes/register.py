from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, EmailStr
from sqlmodel import Session, select

from tables.user import User
from authentication.auth import Auth
from config.db_settings import engine
from config.error_messages import (
    USER_WITH_THIS_EMAIL_ALREADY_EXISTS,
    USER_WITH_THIS_USERNAME_ALREADY_EXISTS,
)

router = APIRouter()
auth_handler = Auth()


class UserModelRegister(BaseModel):
    email: EmailStr
    username: str | None = None
    password: str = Field(min_length=8)


class RegisterHandler:

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    def check_email(self, session):
        statement = select(User).where(User.email == self.email)
        if session.exec(statement).first():
            raise HTTPException(
                status_code=401,
                detail=USER_WITH_THIS_EMAIL_ALREADY_EXISTS)
        else:
            return True

    def check_username(self, session):
        statement = select(User).where(User.username == self.username)
        if session.exec(statement).first():
            raise HTTPException(
                status_code=401,
                detail=USER_WITH_THIS_USERNAME_ALREADY_EXISTS)
        else:
            return True

    def user_not_exists(self):
        with Session(engine) as session:
            return self.check_email(session) and \
                   self.check_username(session)

    def create_user(self):
        return User(
            username=self.username,
            email=self.email,
            password=self.password,
        )


@router.post("/signup")
async def registration(user: UserModelRegister):
    password = auth_handler.encode_password(user.password)
    register_handler = RegisterHandler(user.email, user.username, password)
    user_db = register_handler.create_user()
    if register_handler.user_not_exists():
        with Session(engine) as session:
            session.add(user_db)
            session.commit()
    return {"message": "Registration successful"}
