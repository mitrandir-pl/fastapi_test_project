import os

from dotenv import load_dotenv
from sqlmodel import create_engine, Session

from tables.user import init_users_table
from tables.post import init_posts_table


load_dotenv()


DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    init_users_table(engine)
    init_posts_table(engine)
