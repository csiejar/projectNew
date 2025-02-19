from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(debug=True)

# 靜態檔案（提供 HTML、CSS、JS）
app.mount("/static", StaticFiles(directory="static"), name="static")

# 題庫資料（模擬數據）
questions = [
    {"id": 1, "question": "2 + 2 = ?", "options": ["3", "4", "5", "6"], "answer": "4"},
    {"id": 2, "question": "5 + 3 = ?", "options": ["5", "7", "8", "9"], "answer": "8"},
]

# API - 獲取題目
@app.get("/api/questions")
async def get_questions():
    return JSONResponse(content={"questions": questions})

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
    uvicorn.run(app, host="0.0.0.0", port=8000)