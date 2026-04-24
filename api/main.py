import os
import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo_client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
mongo_db = mongo_client[os.getenv("MONGO_DB_NAME", "blog_db")]


def get_mysql_connection():
    return mysql.connector.connect(
        database=os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        host=os.getenv("MYSQL_HOST"),
    )


@app.get("/users")
async def get_users():
    conn = None
    cursor = None
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nom, email, created_at FROM utilisateurs ORDER BY id")
        records = cursor.fetchall()
        return {"users": records}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"MySQL error: {exc}") from exc
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.get("/posts")
async def get_posts():
    try:
        posts = await mongo_db.posts.find({}, {"_id": 0}).to_list(length=100)
        return {"posts": posts}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Mongo error: {exc}") from exc
