from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
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
    userImg = Column(String(255))
    topic_stats = Column(JSON)  # 儲存使用者對各主題的答題統計

# 首頁下方大主題資料表
class topicsSQL(Base):
    __tablename__ = 'topics'
    topicID = Column(Integer, primary_key=True)
    title = Column(String(255))
    content = Column(Text)
    link = Column(String(255))
    img = Column(String(255))

# 題庫資料表
class questionsSQL(Base):
    __tablename__ = 'questions'
    questionID = Column(Integer, primary_key=True)
    topicID = Column(Integer)
    question = Column(Text)
    optionA = Column(Text)
    optionB = Column(Text)
    optionC = Column(Text)
    optionD = Column(Text)
    answer = Column(String(1))
    image = Column(String(512))
    source = Column(String(255))

# 留言討論區資料表
class commentsSQL(Base):
    __tablename__ = 'comments'
    commentID = Column(Integer, primary_key=True)
    questionID = Column(Integer)
    userID = Column(String(255))
    comment = Column(Text)

# 權限設定資料表
class permissionSQL(Base):
    __tablename__ = 'permission'
    permissionID = Column(Integer, primary_key=True)
    permissionDetails = Column(String(100))
    permissionUser = Column(String(100))
    allowLink = Column(String(100))

class answerRecordsSQL(Base):
    __tablename__ = 'answer_records'
    recordID = Column(Integer, primary_key=True)
    userID = Column(String(255))
    answers = Column(JSON)
    timestamp = Column(DateTime)