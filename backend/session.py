from pydantic import BaseModel
from fastapi import HTTPException, FastAPI, Response, Depends, APIRouter
from uuid import UUID, uuid4

from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters


class SessionData(BaseModel):
    sessionToken: str  # 確保變數名稱與 create_session() 內一致


cookie_params = CookieParameters(
    httponly=True,  # 限制只能透過 HTTP 請求讀取
    secure=False,   #!!!開發結束後要改成True 
    max_age=3600,   # Session 存活時間 (1 小時)
    samesite="lax", # 跨站請求安全策略
)

# 使用 UUID 來標識 session
cookie = SessionCookie(
    cookie_name="session_id",
    identifier="general_verifier",
    auto_error=True,
    secret_key="1234567890qwertyuiopasdfghjklzxcvbnm",  # ❗請使用強隨機字串
    cookie_params=cookie_params,
)

# FastAPI Sessions 記憶體後端
backend = InMemoryBackend[UUID, SessionData]()


class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, SessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """如果 session 存在，則驗證成功"""
        return True


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)

router = APIRouter()


@router.post("/create_session/{token}")
async def create_session(token: str, response: Response):
    session = uuid4()
    data = SessionData(sessionToken=token)  # ❗確保變數名稱與 SessionData 類別一致
    await backend.create(session, data)
    cookie.attach_to_response(response, session)
    return {"message": "Session created successfully", "session_id": str(session)}


@router.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    print(session_data)
    return {"sessionToken": session_data.sessionToken}


@router.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return {"message": "Session deleted successfully"}