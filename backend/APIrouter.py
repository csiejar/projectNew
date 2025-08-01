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
async def editQuestion(request: EditQuestionRequest, userToken: str = Depends(findTokenFromCookies)):
    if userToken and (userToken != "None"):
        try:
            userID = dbMain.getUserDataByToken(userToken)["userID"]
            if dbMain.isUserAllowToAccessLink(userID, "editQuestion"):
                update_data = {k: v for k, v in request.model_dump().items() if v is not None}
                try:
                    dbMain.editQuestion(**update_data)
                    return {"message": "編輯問題成功"}
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            else:
                return JSONResponse(content={"message": "無權限"}, status_code=403)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

        
    
class DeleteQuestionRequest(BaseModel):
    questionID: int
@router.post("/deleteQuestion")
async def deleteQuestion(request: DeleteQuestionRequest, userToken: str = Depends(findTokenFromCookies)):
    if userToken and (userToken != "None"):
        try:
            userID = dbMain.getUserDataByToken(userToken)["userID"]
            if dbMain.isUserAllowToAccessLink(userID, "deleteQuestion"):
                try:
                    dbMain.deleteQuestion(request.questionID)
                    return {"message": "刪除問題成功"}
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            else:
                return JSONResponse(content={"message": "無權限"}, status_code=403)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    
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
async def addQuestion(request: addQuestionRequest, userToken: str = Depends(findTokenFromCookies)):
    if userToken and (userToken != "None"):
        try:
            userID = dbMain.getUserDataByToken(userToken)["userID"]
            if dbMain.isUserAllowToAccessLink(userID, "addQuestion"):
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
            else:
                return JSONResponse(content={"message": "無權限"}, status_code=403)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
@router.get("/isPermitted")
async def isPermitted(link: str, userToken: str = Depends(findTokenFromCookies)):
    if userToken and (userToken != "None"):
        try:
            userID = dbMain.getUserDataByToken(userToken)["userID"]
            if dbMain.isUserAllowToAccessLink(userID, link):
                return JSONResponse(content={"message": "有權限"}, status_code=200)
            else:
                return JSONResponse(content={"message": "無權限"}, status_code=403)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router.get("/getAllPermissions")
async def getAllPermissions():
    try:
        permissions = dbMain.getAllPermissionDetails()
        return JSONResponse(content=permissions, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/getAllUsersIDAndName")
async def getAllUsersIDAndName():
    try:
        users = dbMain.getAllUsersIDAndName()
        return JSONResponse(content=users, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class addPermissionRequest(BaseModel):
    userID: str
    permissionID: int
@router.post("/addPermission")
async def addPermission(request: addPermissionRequest, userToken: str = Depends(findTokenFromCookies)):
    permissionID = request.permissionID
    userID = request.userID
    if userToken and (userToken != "None"):
        try:
            operatorUserID = dbMain.getUserDataByToken(userToken)["userID"]
            if dbMain.isUserAllowToAccessLink(operatorUserID, "addPermission"):
                try:
                    requestData = dbMain.addUserToPermission(permissionID, userID)
                    if requestData == "用戶已有權限":
                        return JSONResponse(content={"message": "用戶已有權限"}, status_code=200)
                    if requestData:
                        return JSONResponse(content={"message": "新增權限成功"}, status_code=200)
                    else:
                        return JSONResponse(content={"message": "新增權限失敗"}, status_code=500)
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            else:
                return JSONResponse(content={"message": "無權限"}, status_code=403)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    

@router.get("/getQuestionsForQuestionPage")
async def getQuestionsForQuestionPage():
    try:
        questions = dbMain.getQuestionsForQuestionPage()[0:50]
        return JSONResponse(content=questions, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class submitAnswerRequest(BaseModel):
    usersAnswer: dict
@router.post("/submitAnswer")
async def submitAnswer(request: submitAnswerRequest, userToken: str = Depends(findTokenFromCookies)):
    if userToken and (userToken != "None"):
        try:
            userID = dbMain.getUserDataByToken(userToken)["userID"]
            recordID =  dbMain.uploadUsersAnswer(userID, request.usersAnswer)
            return JSONResponse(content={"message": "提交答案成功", "recordID": recordID}, status_code=200)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router.get("/getAnswerRecord/{recordID}")
async def getAnswerRecord(recordID):
    try:
        record = dbMain.getAnswerRecord(recordID)
        if record:
            return JSONResponse(content={"message":"success","record":record}, status_code=200)
        else:
            raise HTTPException(status_code=404, detail="Record not found")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        

@router.get("/getQuestionsForAnswerRecord/{recordID}")
async def getQuestionsForAnswerRecord(recordID):
    try:
        questions = dbMain.getQuestionsForAnswerRecord(recordID)
        if questions:
            return JSONResponse(content={"message":"success","questions":questions}, status_code=200)
        else:
            raise HTTPException(status_code=404, detail="Questions not found for this record")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        
@router.get("/getUserAnswerRecord")
async def getUserAnswerRecord(userToken: str = Depends(findTokenFromCookies)):
    if userToken and (userToken != "None"):
        try:
            userID = dbMain.getUserDataByToken(userToken)["userID"]
            records = dbMain.getUserAnswerRecord(userID)
            return JSONResponse(content={"message":"success","records":records}, status_code=200)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router.get("/getUserTopicsCorrectRate") # 取得使用者各單元答題正確率
async def getUserTopicsCorrectRate(userToken: str = Depends(findTokenFromCookies)):
    if userToken and (userToken != "None"):
        try:
            userID = dbMain.getUserDataByToken(userToken)["userID"]
            topics_correct_rate = dbMain.getUserTopicsCorrectRate(userID)
            topicTitles = dbMain.getAllTopicsTitleWithID()
            return JSONResponse(content={"message":"success","topics_correct_rate":topics_correct_rate,"topicTitles":topicTitles}, status_code=200)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.get("/getSelectedQuestion") # 依照使用者選擇的單元取得問題
async def getSelectedQuestion(topicIDs: str, questionCount: int):
    # 將 topicIDs 轉換為列表
    topicIDs = topicIDs.strip("[]").split(",") if topicIDs else []

    try:
        if not topicIDs or not questionCount:
            raise HTTPException(status_code=400, detail="請提供有效的單元ID和問題數量")
        questions = dbMain.getSelectedQuestion(topicIDs, questionCount)
        if not questions:
            raise HTTPException(status_code=404, detail="沒有找到符合條件的問題")
        return JSONResponse(content={"message":"success","questions":questions}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/getTopicsForQuestionSelector")
async def getTopicsForQuestionSelector():
    try:
        topics = dbMain.getTopicsForQuestionSelector()
        if not topics:
            raise HTTPException(status_code=404, detail="沒有找到任何單元")
        return JSONResponse(content={"message":"success","topics":topics}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))