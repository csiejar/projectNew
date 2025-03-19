from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="./frontend/templates")

@router.get("/")  # 首頁
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

