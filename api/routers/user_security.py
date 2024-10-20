from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users.authentication import RedisStrategy
from redis import get_redis_strategy
from config import SECRET_KEY, ALGORITHM
from jose import jwt

router = APIRouter()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), redis: RedisStrategy = Depends(get_redis_strategy())):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    await redis.set(f"user_token:{user.username}", access_token, ex=3600)

    return {"access_token": access_token, "token_type": "bearer"}

def authenticate_user(username: str, password: str):
    if username == "hakie" and password == "password":
        return {username: "hakie"}

    return None

def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)