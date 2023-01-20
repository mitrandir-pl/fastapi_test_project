from fastapi import APIRouter, Depends
from sqlmodel import Session

from services.users_handler import UserOutModel, UsersHandler, UserListOutModel
from config.db_settings import get_session


router = APIRouter()


@router.get("/users")
async def get_users_list(session: Session = Depends(get_session)) -> list[UserListOutModel]:
    return UsersHandler().get_users_list(session)


@router.get("/users/{user_id}")
async def get_post_by_id(user_id: int, session: Session = Depends(get_session)) -> UserOutModel:
    return UsersHandler().get_user_by_id(user_id, session)
