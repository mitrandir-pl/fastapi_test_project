from fastapi import APIRouter, Depends

from authentication.jwt_bearer import JWTBearer
from pydantic import BaseModel
from services.post_handler import PostsHandler, PostModel
from tables.post import Post
from config.error_messages import (
    POST_CREATED_MESSAGE,
    POST_UPDATED_MESSAGE,
    POST_DELETED_MESSAGE,
)


router = APIRouter()


class PostsResponseModel(BaseModel):
    message: str


@router.get("/posts")
async def get_posts_list() -> list[Post]:
    return PostsHandler().get_posts_list()


@router.get("/posts/{post_id}")
async def get_post_by_id(post_id: int) -> Post:
    return PostsHandler().get_post_by_id(post_id)


@router.post("/posts")
async def create_post(post: PostModel,
                      token: str = Depends(JWTBearer())) -> PostsResponseModel:
    PostsHandler().create_post(post, token)
    return PostsResponseModel(message=POST_CREATED_MESSAGE)


@router.put("/posts/{post_id}")
async def update_post(post_id: int, post: PostModel,
                      token: str = Depends(JWTBearer())) -> PostsResponseModel:
    PostsHandler().update_post(post, post_id, token)
    return PostsResponseModel(message=POST_UPDATED_MESSAGE)


@router.delete("/posts/{post_id}")
async def delete_post(post_id: int,
                      token: str = Depends(JWTBearer())) -> PostsResponseModel:
    PostsHandler().delete_post(post_id, token)
    return PostsResponseModel(message=POST_DELETED_MESSAGE)


@router.post("/posts/{post_id}/set_like")
async def set_like(post_id: int,
                   token: str = Depends(JWTBearer())) -> PostsResponseModel:
    message = PostsHandler().set_like(post_id, token)
    return PostsResponseModel(message=message)
