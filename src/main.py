import os

from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel
from dotenv import load_dotenv

from tables.user import init_users_table
from tables.post import init_posts_table
from routes import register

load_dotenv()
app = FastAPI()

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


@app.get("/")
async def home():
    return {"hello": "world"}


if __name__ == "__main__":
    init_db()
    init_users_table(engine)
    init_posts_table(engine)
