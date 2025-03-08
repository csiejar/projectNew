from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 設定資料庫連接
DATABASE_URL = "mysql+pymysql://hankbeststudent:aP7Xq9T2mB5L3Y6Z@23.146.248.32/GraduationProject"
engine = create_engine(DATABASE_URL, pool_recycle=36000)

# 定義資料表
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    userID = Column(String, primary_key=True)
    googleID = Column(String)
    name = Column(String)
    email = Column(String)
    sessionToken = Column(String)
    recoveryToken = Column(String)
    sex = Column(String)

Base.metadata.create_all(bind=engine)

def isConnected():
    try:
        # 資料庫連接
        Session = sessionmaker(bind=engine)
        session = Session()
        return "資料庫狀態: 已連線成功"
    except Exception as e:
        return "資料庫狀態: 連線失敗 因為: " + str(e)
    finally:
        session.close()

print(isConnected())