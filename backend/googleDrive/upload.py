from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from generator import generateTempFileName
from pydantic import BaseModel
router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB 限制

@router.post("/uploadfile")
async def upload_file(file: UploadFile = File(...)):
    # 檢查檔案類型
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(413,"檔案類型錯誤，僅支援 JPEG 和 PNG 格式。")
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(413,"檔案大小超過限制，請上傳小於 10MB 的檔案。")
    # 儲存檔案
    with open(f"backend/googleDrive/readyForUpload/{file.filename}", "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    return {"filename": file.filename}

class UploadRequest(BaseModel):
    topicID: int
    fileName: str
@router.post("/uploadToDrive")
async def uploadToDrive(request: UploadRequest):
    questionID = generateTempFileName()
    imagePath = f"backend/googleDrive/readyForUpload/{request.fileName}"
    from backend.googleDrive.drive import uploadQuestionImage
    try:
        url = uploadQuestionImage(request.topicID,questionID,imagePath)
        if url["status"] == "success":
            return JSONResponse(status_code=200, content={"message": url["message"], "url": f"https://hank.ezborrow.tw/img/{request.topicID}/{questionID}.png"})
        else:
            raise HTTPException(status_code=500, detail=url["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))