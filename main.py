from fastapi import FastAPI, Depends, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
try:
    from ./ import models
    from .database import engine, SessionLocal
except ImportError:
    import models
    from database import engine, SessionLocal
from sqlalchemy.orm import Session

try:
    models.Base.metadata.create_all(bind=engine)
except Exception as error:
    print("Database initialization failed")
    print("Error: ", error)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int = None

try:
    conn = psycopg2.connect(
        host='localhost',
        database='fastapi',
        user='postgres',
        password='Hp@123',
        cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful")
except Exception as error:
    print("Database connection failed")
    print("Error: ", error)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2 }]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
@app.get("/")
def root():
    return {"message": " welcome to my api!!"}

@app.get("/sqlalchemy")
def test_posts(db: SessionLocal = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status": "success"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    print(id)
    post = find_post(id)
    return{"post": post}

