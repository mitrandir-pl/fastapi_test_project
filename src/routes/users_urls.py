from fastapi import APIRouter

from services.users_handler import UserOutModel, UsersHandler, UserListOutModel


router = APIRouter()


@router.get("/users")
async def get_users_list() -> list[UserListOutModel]:
    return UsersHandler().get_users_list()


@router.get("/users/{user_id}")
async def get_post_by_id(user_id: int) -> UserOutModel:
    return UsersHandler().get_user_by_id(user_id)
