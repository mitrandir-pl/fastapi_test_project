from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import Session

from authentication.auth import Auth
from config.db_settings import engine
from services.register_handler import UserModelRegister, RegisterHandler
from config.error_messages import SUCCESSFUL_REGISTER_MESSAGE


router = APIRouter()
auth_handler = Auth()


class RegisterResponseModel(BaseModel):
    message: str


@router.post("/signup")
async def registration(user: UserModelRegister) -> RegisterResponseModel:
    password = auth_handler.encode_password(user.password)
    register_handler = RegisterHandler(user.email, user.username, password)
    user_db = register_handler.create_user()
    if register_handler.user_not_exists():
        with Session(engine) as session:
            session.add(user_db)
            session.commit()
    return RegisterResponseModel(message=SUCCESSFUL_REGISTER_MESSAGE)
