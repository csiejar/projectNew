# router.py
from fastapi import APIRouter, HTTPException, Response , Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .database import dbMain
from dotenv import load_dotenv
import os
from google.oauth2 import id_token
from google.auth.transport import requests
load_dotenv()
from cookies import *


router = APIRouter()

# API - 登入
class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(request: LoginRequest):
    if request.username != "admin" or request.password != "admin":
        return JSONResponse(content={"message": "登入失敗"}, status_code=401)
    else:
        return JSONResponse(content={"message": "登入成功"})
    
@router.get("/getAllTopics")
async def getAllTopics():
    try:
        topics = dbMain.getAllTopics()
        return JSONResponse(content=topics, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class GoogleLoginRequest(BaseModel):
    token: str
@router.post("/googleLogin")
async def googleLogin(request: GoogleLoginRequest):
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    try:
        # 驗證 Token
        id_info = id_token.verify_oauth2_token(request.token, requests.Request(), GOOGLE_CLIENT_ID)
        # 取得使用者資訊
        user_id = id_info["sub"]  # Google User ID
        email = id_info["email"]
        name = id_info["name"]
        # # 檢查使用者是否已存在於資料庫
        isUserExisted, originalSessionToken = dbMain.checkUserExist(user_id)
        if isUserExisted:
            # 使用者已存在，更新 sessionToken
            sessionToken = dbMain.updateUserSessionToken(originalSessionToken)
            return setTokenToCookies(sessionToken)
        else:
            # 使用者不存在，新增使用者
            newuser = dbMain.createUser(user_id, name, email)
            return setTokenToCookies(newuser["sessionToken"])
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Google token")
    
@router.get("/authUser")
async def authUser(userToken: str = Depends(findTokenFromCookies)):
    if userToken and (userToken != "None"):
        userData = dbMain.getUserDataByToken(userToken)
        return JSONResponse(content={"message": "已登入", "userData":userData}, status_code=200, headers={"Content-Type": "application/json; charset=utf-8"})
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.get("/getUserInfoByToken")
async def getUserInfoByToken(userToken: str):
    if userToken and (userToken != "None"):
        userData = dbMain.getUserDataByToken(userToken)
        return JSONResponse(content=userData, status_code=200, headers={"Content-Type": "application/json; charset=utf-8"})
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.post("/logout")
async def logout():
    deleteCookies()
    return JSONResponse(content={"message": "登出成功"}, status_code=200 , headers={"Content-Type": "application/json; charset=utf-8"})
@router.get("/getAllQuestions")
async def getAllQuestions():
    try:
        questions = dbMain.getAllQuestions()
        return JSONResponse(content=questions, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/submitComment")
async def submitComment(questionID: int, comment: str, userToken: str = Depends(findTokenFromCookies)):
    if userToken and (userToken != "None"):
        try:
            userID = dbMain.getUserInfoByToken(userToken)["userID"]
            dbMain.Comment(questionID,userID ,comment)
            return JSONResponse(content={"message": "留言成功"}, status_code=200)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router.get("/getAllComments")
async def getAllComments():
    try:
        comments = dbMain.getAllComments()
        return JSONResponse(content=comments, status_code=200, headers={"Content-Type": "application/json; charset=utf-8"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/getCommentsByQuestionID")
async def getCommentsByQuestionID(questionID: int):
    try:
        comments = dbMain.getCommentsByQuestionID(questionID)
        return JSONResponse(content=comments, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))