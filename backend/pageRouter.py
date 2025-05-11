from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

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