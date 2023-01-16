from fastapi import FastAPI
from config.db_settings import init_db

from routes import register
from routes import login


app = FastAPI()
app.include_router(register.router)
app.include_router(login.router)


@app.get("/")
async def home():
    return {"hello": "world"}


if __name__ == "__main__":
    init_db()
