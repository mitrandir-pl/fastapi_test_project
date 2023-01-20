from fastapi import FastAPI
from sqlmodel import Session

from config.db_settings import init_db, engine, get_session
from routes import register, login, posts_urls, users_urls


app = FastAPI()
app.include_router(register.router)
app.include_router(login.router)
app.include_router(posts_urls.router)
app.include_router(users_urls.router)


app.dependency_overrides[get_session] = get_session


@app.get("/")
async def home():
    return {"hello": "world"}


if __name__ == "__main__":
    init_db()
