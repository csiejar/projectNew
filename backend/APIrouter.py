# router.py
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .database import dbMain
from dotenv import load_dotenv
import os
from google.oauth2 import id_token
from google.auth.transport import requests
load_dotenv()
from session import *


router = APIRouter()

# API - 登入
class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/api/login")
async def login(request: LoginRequest):
    if request.username != "admin" or request.password != "admin":
        return JSONResponse(content={"message": "登入失敗"}, status_code=401)
    else:
        return JSONResponse(content={"message": "登入成功"})
    
@router.get("/api/getAllTopics")
async def getAllTopics():
    try:
        topics = dbMain.getAllTopics()
        return JSONResponse(content=topics, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class GoogleLoginRequest(BaseModel):
    token: str
@router.post("/api/googleLogin")
async def googleLogin(request: GoogleLoginRequest):
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    try:
        # 驗證 Token
        id_info = id_token.verify_oauth2_token(request.token, requests.Request(), GOOGLE_CLIENT_ID)
        # 取得使用者資訊
        user_id = id_info["sub"]  # Google User ID
        email = id_info["email"]
        name = id_info["name"]
        # TODO session待研究
        # # 檢查使用者是否已存在於資料庫
        isUserExisted, sessionToken = dbMain.checkUserExist(user_id)
        # print(isUserExisted, sessionToken)
        if isUserExisted:
            # 使用者已存在，更新 sessionToken
            # print(await create_session(sessionToken, response=Response()))
            return sessionToken
        else:
            # 使用者不存在，新增使用者
            newuser = dbMain.createUser(user_id, name, email)
            return await create_session(newuser.sessionToken, response=Response())
        return {
            "message": "Google login successful",
            "user_id": user_id,
            "email": email,
            "name": name
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Google token")
    