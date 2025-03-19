from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .dbClass import *
from fastapi import HTTPException

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
