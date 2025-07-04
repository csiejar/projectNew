from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import os

router = APIRouter()
templates = Jinja2Templates(directory="./frontend/templates")

@router.get("/")  # 首頁
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/questionAdmin") # 問題管理頁面
async def questionAdmin(request: Request):
    return templates.TemplateResponse("questionAdmin/index.html", {"request": request})

@router.get("/question") # 問題編輯頁面
async def questionEdit(request: Request):
    return templates.TemplateResponse("question/index.html", {"request": request})

@router.get("/permissionAdmin") # 權限管理頁面
async def permissionAdmin(request: Request):
    return templates.TemplateResponse("permissionAdmin/index.html", {"request": request})

@router.get("/answerRecord/{questionID}")  # 回答紀錄頁面
async def answerRecord(request: Request, questionID: int):
    return templates.TemplateResponse("answerRecord/index.html", {"request": request, "questionID": questionID})

@router.get("/userAnswerRecord")  # 回答紀錄頁面
async def userAnswerRecord(request: Request):
    return templates.TemplateResponse("userAnswerRecord/index.html", {"request": request})

@router.get("/correctRate")  # 回答紀錄頁面
async def correctRate(request: Request):
    return templates.TemplateResponse("correctRate/index.html", {"request": request})

@router.get("/questionSelector")  # 使用者選擇問題頁面
async def questionSelector(request: Request):
    return templates.TemplateResponse("questionSelector/index.html", {"request": request})

@router.get("/img/{img_path:path}")  # 圖片路由，支援子資料夾
async def img(img_path: str):
    img_full_path = os.path.join("img", img_path)
    if not os.path.isfile(img_full_path):
        return {"error": "Image not found"}
    return FileResponse(img_full_path)