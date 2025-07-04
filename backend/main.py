import os
import sys
import subprocess

# 確保安裝 `requirements.txt` 內的套件
def install_requirements():
    # 檢查是否已經執行過套件安裝（避免重複執行）
    if hasattr(install_requirements, '_already_executed'):
        print("🔄 套件安裝已執行過，跳過...")
        return
    
    req_file = "backend/requirements.txt"
    if os.path.exists(req_file):
        print("🔍 檢查並安裝需求套件...")
        try:
            # 修正 pip 指令，移除 pip3
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
            print("✅ 所有套件已安裝！")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ 安裝 `requirements.txt` 失敗：{e}")
            print("請手動執行 `pip install -r requirements.txt`")
    else:
        print("⚠️ 找不到 requirements.txt 檔案")
    
    # 標記已執行過
    install_requirements._already_executed = True

# 只在主程式啟動時執行套件安裝檢查
if __name__ == "__main__":
    print("開始執行套件安裝檢查...")
    install_requirements()
    print("套件安裝檢查完成，繼續載入應用程式...")

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import platform
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.APIrouter import router as APIRouter  # For API use
from backend.pageRouter import router as pageRouter # For page use
from backend.googleDrive.upload import router as googleDriveRouter # For Google Drive use

app = FastAPI(debug=True)

# 靜態檔案（提供 HTML、CSS、JS）
app.mount("/static", StaticFiles(directory="./frontend/static"), name="static")

# 註冊 router
app.include_router(APIRouter, prefix="/api")
app.include_router(pageRouter)
app.include_router(googleDriveRouter)


# 啟動 FastAPI
if __name__ == "__main__":
    import uvicorn
    # uvicorn.run("main:app",host='0.0.0.0',port=8000, reload=True)
    uvicorn.run("main:app",port=8000, reload=True)
