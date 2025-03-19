from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import platform
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.APIrouter import router  # 確保只匯入 router，而不是 *


app = FastAPI(debug=True)

# 靜態檔案（提供 HTML、CSS、JS）
app.mount("/static", StaticFiles(directory="./frontend/static"), name="static")

# 註冊 router
app.include_router(router)

if __name__ == "__main__":
    if platform.system() == "Windows":
        os.system("run.bat")
    if platform.system() in ["Darwin", "Linux"]:
        os.system("chmod +x run.sh")
        os.system("./run.sh")