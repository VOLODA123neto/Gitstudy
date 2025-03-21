from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List

app = FastAPI()

# Модель користувача
class User(BaseModel):
    id: int
    username: str
    email: EmailStr

# Схема для створення користувача (без id)
class UserCreate(BaseModel):
    username: str
    email: EmailStr

# Фейковий список користувачів
users = [
    User(id=1, username="user1", email="user1@example.com"),
    User(id=2, username="user2", email="user2@example.com"),
]

# Отримати список всіх користувачів
@app.get("/users", response_model=List[User])
def get_users():
    return users

# Отримати користувача за id
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Створити нового користувача
@app.post("/create_user", response_model=User)
def create_user(user: UserCreate):
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=user.username, email=user.email)
    users.append(new_user)
    return new_user