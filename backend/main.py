import os
import sys
import subprocess

# 確保安裝 `requirements.txt` 內的套件
def install_requirements():
    req_file = "requirements.txt"
    if os.path.exists(req_file):
        print("🔍 檢查並安裝需求套件...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
            print("✅ 所有套件已安裝！")
        except subprocess.CalledProcessError:
            print("⚠️ 安裝 `requirements.txt` 失敗，請手動執行 `pip install -r requirements.txt`")

install_requirements()

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


# 啟動 FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)