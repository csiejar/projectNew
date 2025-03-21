from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from .dbClass import *
# from dbClass import *
from fastapi import HTTPException
import generator

# 設定資料庫連接
DATABASE_URL = "mysql+pymysql://hank:hankbeststudent@10.147.17.41/hank"
engine = create_engine(DATABASE_URL, pool_recycle=36000)

Base.metadata.create_all(bind=engine)

# 測試連接
def isConnected():
    try:
        # 資料庫連接
        Session = sessionmaker(bind=engine)
        session = Session()
        return "資料庫狀態: 已連線成功"
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="資料庫狀態: 連線失敗",
            headers={"X-Error": str(e)},
        )
    finally:
        session.close()

# 取得所有Users
def getAllUsers():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        users = session.query(UsersSQL).all()
        # 將資料轉換為字典格式
        users = [
            {
                "userID": user.userID,
                "googleID": user.googleID,
                "name": user.name,
                "email": user.email,
                "sessionToken": user.sessionToken,
                "recoveryCode": user.recoveryCode,
            }
            for user in users
        ]
        return users
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

# 取得所有Topics
def getAllTopics():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        topics = session.query(topicsSQL).all()
        # 將資料轉換為字典格式

        topics = [
            {
                "topicID": topic.topicID,
                "title": topic.title,
                "content": topic.content,
                "link": topic.link,
                "img": topic.img,
            }
            for topic in topics
        ]
        return topics
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

# 建立使用者
def createUser(googleID, name, email):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        new_user = UsersSQL(
            userID=generator.userID,
            googleID=googleID,
            name=name,
            email=email,
            sessionToken=generator.sessionToken,
            recoveryCode=generator.recoveryCode,
            sex=0 # 不願透露-0 男-1 女-2
        )
        session.add(new_user)
        session.commit()
        return {"name": new_user.name, "sessionToken": new_user.sessionToken, "recoveryCode": new_user.recoveryCode}
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

# 確認使用者是否存在
def checkUserExist(googleID):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(UsersSQL).filter_by(googleID=googleID).first()
        if user:
            return True,user.sessionToken
        else:
            return False,None
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def getUserInfoByToken(token):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(UsersSQL).filter_by(sessionToken=token).first()
        if user:
            return {
                "userID": user.userID,
                "name": user.name,
                "email": user.email,
                "sex": user.sex
            }
        else:
            return None
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()