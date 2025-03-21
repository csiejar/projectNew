from fastapi import Cookie, HTTPException
from fastapi.responses import JSONResponse

def setTokenToCookies(sessionToken: str):
    contents = {"sessionToken": sessionToken}
    response = JSONResponse(content=contents)
    response.set_cookie(key="sessionToken", value=sessionToken, max_age=3600, httponly=False)
    return response

def deleteCookies():
    contents = False
    response = JSONResponse(content=contents)
    response.delete_cookie(key="sessionToken")
    return response


def findTokenFromCookies(sessionToken: str = Cookie("None")):
    if not sessionToken:
        raise HTTPException(status_code=401, detail="No session token found")
    return sessionToken
