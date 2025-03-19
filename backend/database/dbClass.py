from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 定義資料表
Base = declarative_base()

# 使用者資料表
class UsersSQL(Base):
    __tablename__ = 'users'
    userID = Column(String(255), primary_key=True)
    googleID = Column(String(255))
    name = Column(String(255))
    email = Column(String(255), unique=True)
    sessionToken = Column(String(255))
    recoveryCode = Column(String(255))
    sex = Column(Integer)

# 首頁下方大主題資料表
class topicsSQL(Base):
    __tablename__ = 'topics'
    topicID = Column(Integer, primary_key=True)
    title = Column(String(255))
    content = Column(Text)
    link = Column(String(255))
    img = Column(String(255))