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
from typing import Optional


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
        userImg = id_info["picture"]
        # # 檢查使用者是否已存在於資料庫
        isUserExisted, originalSessionToken = dbMain.checkUserExist(user_id)
        if isUserExisted:
            # 使用者已存在，更新 sessionToken
            sessionToken = dbMain.updateUserSessionToken(originalSessionToken)
            return setTokenToCookies(sessionToken)
        else:
            # 使用者不存在，新增使用者
            newuser = dbMain.createUser(user_id, name, email, userImg)
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
async def getUserInfoByToken(userToken: str = Depends(findTokenFromCookies)):
    if userToken and (userToken != "None"):
        userData = dbMain.getUserDataByToken(userToken)
        return JSONResponse(content=userData, status_code=200, headers={"Content-Type": "application/json; charset=utf-8"})
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.post("/logout")
async def logout():
    return deleteCookies()
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
            userID = dbMain.getUserDataByToken(userToken)["userID"]
            dbMain.Comment(questionID,userID ,comment)
            return JSONResponse(content={"message": "留言成功"}, status_code=200)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router.get("/getSixComments")
async def getSixComments():
    try:
        comments = dbMain.getSixComments()
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
    
class EditQuestionRequest(BaseModel):
    questionID: int  # 這個是必要的，因為要識別要修改哪一題
    topicID: Optional[int] = None
    question: Optional[str] = None
    optionA: Optional[str] = None
    optionB: Optional[str] = None
    optionC: Optional[str] = None
    optionD: Optional[str] = None
    answer: Optional[str] = None
    image: Optional[str] = None
    source: Optional[str] = None

@router.post("/editQuestion")
async def editQuestion(request: EditQuestionRequest):
    update_data = {k: v for k, v in request.model_dump().items() if v is not None}
    try:
        dbMain.editQuestion(**update_data)
        return {"message": "編輯問題成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class DeleteQuestionRequest(BaseModel):
    questionID: int
@router.post("/deleteQuestion")
async def deleteQuestion(request: DeleteQuestionRequest):
    try:
        dbMain.deleteQuestion(request.questionID)
        return {"message": "刪除問題成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class addQuestionRequest(BaseModel):
    topicID: int
    question: str
    optionA: str
    optionB: str
    optionC: str
    optionD: str
    answer: str
    image: Optional[str] = ""
    source: Optional[str] = ""
@router.post("/addQuestion")
async def addQuestion(request: addQuestionRequest):
    try:
        dbMain.addQuestion(
            topicID=request.topicID,
            question=request.question,
            optionA=request.optionA,
            optionB=request.optionB,
            optionC=request.optionC,
            optionD=request.optionD,
            answer=request.answer,
            image=request.image,
            source=request.source
        )
        return {"message": "新增問題成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))