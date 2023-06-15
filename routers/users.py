from fastapi import APIRouter, Depends
from utils.api import USER_MS_URL
from utils.security import oauth2_scheme
from schemas.users import *
import httpx

router = APIRouter()

@router.get("/login")
async def login(username: str, password: str):
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "username": username,
        "password": password
    }
    async with httpx.AsyncClient() as client:
        ans = httpx.post(USER_MS_URL + "/login", json=body, headers=headers) 
    return ans.json()

@router.post("/register")
async def register(register: Register):
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "username": register.username,
        "password": register.password,
        "mail": register.email,
        "birthdate": {"$date": register.birthdate}
    }
    async with httpx.AsyncClient() as client:
        ans = httpx.post(USER_MS_URL + "/register", json=body, headers=headers)
    if ans.status_code == 500:
        return {"error": ans.text}
    return ans.json()

@router.get("/user")
async def get_user(token: str = Depends(oauth2_scheme)):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    async with httpx.AsyncClient() as client:
        ans = httpx.get(USER_MS_URL + "/user", headers=headers)
    return ans.json()

