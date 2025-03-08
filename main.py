from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(debug=True)

# 靜態檔案（提供 HTML、CSS、JS）
app.mount("/static", StaticFiles(directory="static"), name="static")

# Router Settings
templates = Jinja2Templates(directory="templates")

@app.get("/") # 首頁
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})








# API - 登入
class LoginRequest(BaseModel):
    username: str
    password: str
@app.post("/api/login")
async def login(request:LoginRequest):
    if request.username != "admin" or request.password != "admin":
        return JSONResponse(content={"message": "登入失敗"}, status_code=401)
    else:
        return JSONResponse(content={"message": "登入成功"})

# 啟動服務
if __name__ == "__main__":
    import uvicorn
    import os
    os.system("pip install -r requirements.txt")
    uvicorn.run(app, host="0.0.0.0", port=8000)