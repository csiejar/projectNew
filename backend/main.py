from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import platform
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.APIRouter import router as APIRouter  # For API use
from backend.pageRouter import router as pageRouter # For page use
from backend.session import router as sessionRouter # For session use


app = FastAPI(debug=True)

# 靜態檔案（提供 HTML、CSS、JS）
app.mount("/static", StaticFiles(directory="./frontend/static"), name="static")

# 註冊 router
app.include_router(APIRouter)
app.include_router(pageRouter)
app.include_router(sessionRouter)

# 執行開啟程式
if __name__ == "__main__":
    if platform.system() == "Windows":
        os.system("run.bat")
    if platform.system() in ["Darwin", "Linux"]:
        os.system("chmod +x run.sh")
        os.system("./run.sh")