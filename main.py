from fastapi import FastAPI, Request , HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from google.auth.transport import requests
from google.oauth2 import id_token

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


CLIENT_ID = "1071265157577-7bcbr8qejtvtbmnchgs06ohr9ke46v97.apps.googleusercontent.com"

class TokenData(BaseModel):
    token: str
@app.post("/verify-token")
async def verify_token(data: TokenData):
    try:
        # 驗證 ID Token
        id_info = id_token.verify_oauth2_token(data.token, requests.Request(), CLIENT_ID)
        # 取得用戶資訊
        googleID = id_info["sub"]
        email = id_info["email"]
        name = id_info.get("name", "未知用戶")
        return {"googleID": googleID, "email": email, "name": name}
    
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"驗證失敗: {str(e)}")

# 啟動服務
if __name__ == "__main__":
    import uvicorn
    import os
    os.system("pip install -r requirements.txt")
    uvicorn.run(app, host="127.0.0.1", port=8000)