from fastapi import FastAPI
from .routers import users
import psycopg2
from . import models
from .database import engine
from psycopg2.extras import RealDictCursor

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(users.router)


while True:
    try:
        with psycopg2.connect(
            host="localhost",
            database="task_2",
            user="postgres",
            password="awesome",
            cursor_factory=RealDictCursor,
        ) as conn:
            cursor = conn.cursor()
            print("Connection successful")
            break  # Exit the loop after successful connection
    except psycopg2.OperationalError as error:
        err = error
        print("Failed connecting to database:", err)


@app.get("/api")
def hello_world():
    return {"message": "welcome task 2 Back end !"}
