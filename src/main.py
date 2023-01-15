import os

from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel, Session, Field
from dotenv import load_dotenv

from src.tables.user import init_users_table
from src.tables.post import init_posts_table

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
