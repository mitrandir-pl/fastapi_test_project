from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session

from config.error_messages import WRONG_PASSWORD_MESSAGE
from config.db_settings import get_session
from services.login_handler import LoginHandler, UserLoginModel
from authentication.auth import Auth

router = APIRouter()


class LoginResponseModel(BaseModel):
    refresh_token: str
    access_token: str


class RefreshTokenModel(BaseModel):
    refresh_token: str


class AccessTokenModel(BaseModel):
    access_token: str


@router.post("/login")
async def login(user_credentials: UserLoginModel, session: Session = Depends(get_session)) -> LoginResponseModel:
    login_handler = LoginHandler(
        user_credentials.email,
        user_credentials.password,
    )
    if login_handler.user_exists(session):
        if login_handler.check_password():
            tokens = login_handler.get_tokens()
            return LoginResponseModel(
                refresh_token=tokens["refresh_token"],
                access_token=tokens["access_token"],
            )
        else:
            raise HTTPException(status_code=401,
                                detail=WRONG_PASSWORD_MESSAGE)


@router.get("/refresh_token")
async def refresh_token(token: RefreshTokenModel) -> AccessTokenModel:
    auth_handler = Auth()
    payload = auth_handler.decode_token(token.refresh_token)
    access_token = auth_handler.generate_access_token(payload['user_id'])
    return AccessTokenModel(access_token=access_token)
