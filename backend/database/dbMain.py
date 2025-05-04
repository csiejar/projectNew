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
            return True, user.sessionToken
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

def getUserDataByToken(sessionToken):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(UsersSQL).filter_by(sessionToken=sessionToken).first()
        if user:
            return {
                "userID": user.userID,
                "googleID": user.googleID,
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

def updateUserSessionToken(originalToken):
    newToken = generator.generateSessionToken()
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(UsersSQL).filter_by(sessionToken=originalToken).first()
        if user:
            user.sessionToken = newToken
            session.commit()
            return newToken
        else:
            return False
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def getAllQuestions():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        questions = session.query(questionsSQL).all()
        # 將資料轉換為字典格式
        questions = [
            {
                "questionID": question.questionID,
                "topicID": question.topicID,
                "question": question.question,
                "optionA": question.optionA,
                "optionB": question.optionB,
                "optionC": question.optionC,
                "optionD": question.optionD,
                "answer": question.answer,
                "image": question.image,
                "source": question.source,
            }
            for question in questions
        ]
        return questions
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def checkAnswer(questionID, answer):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        question = session.query(questionsSQL).filter_by(questionID=questionID).first()
        if question:
            if question.answer == answer:
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def addQuestion(topicID: int, question: str, optionA: str, optionB: str, optionC: str, optionD: str, answer: str, image: str, source: str):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        lastQuestionID = session.query(questionsSQL).order_by(questionsSQL.questionID.desc()).first()
        if lastQuestionID:
            questionID = lastQuestionID.questionID + 1
        new_question = questionsSQL(
            questionID=questionID,
            topicID=topicID,
            question=question,
            optionA=optionA,
            optionB=optionB,
            optionC=optionC,
            optionD=optionD,
            answer=answer,
            image=image,
            source=source
        )
        session.add(new_question)
        session.commit()
        return True
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def getAllComments():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        comments = session.query(commentsSQL).all()
        user = session.query(UsersSQL).all()
        # 將資料轉換為字典格式
        comments = [
            {
                "userID": comment.userID,
                "comment": comment.comment,
                "userName": next((u.name for u in user if u.userID == comment.userID), None),
                "questionID": comment.questionID
                # "userImg"
            }
            for comment in comments
        ]
        return comments
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def getCommentsByQuestionID(questionID):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        comments = session.query(commentsSQL).filter_by(questionID=questionID).all()
        # 將資料轉換為字典格式
        comments = [
            {
                "commentID": comment.commentID,
                "questionID": comment.questionID,
                "userID": comment.userID,
                "comment": comment.comment,
            }
            for comment in comments
        ]
        return comments
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def Comment(questionID, userID, comment):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        lastCommentID = session.query(commentsSQL).order_by(commentsSQL.commentID.desc()).first()
        if lastCommentID:
            commentID = lastCommentID.commentID + 1
        new_comment = commentsSQL(
            commentID=commentID,
            questionID=questionID,
            userID=userID,
            comment=comment
        )
        session.add(new_comment)
        session.commit()
        return True
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def editQuestion(questionID: int, topicID: int, question: str, optionA: str, optionB: str, optionC: str, optionD: str, answer: str, image: str, source: str):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        questionToEdit = session.query(questionsSQL).filter_by(questionID=questionID).first()
        if questionToEdit:
            questionToEdit.topicID = topicID
            questionToEdit.question = question
            questionToEdit.optionA = optionA
            questionToEdit.optionB = optionB
            questionToEdit.optionC = optionC
            questionToEdit.optionD = optionD
            questionToEdit.answer = answer
            questionToEdit.image = image
            questionToEdit.source = source
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def deleteQuestion(questionID: int):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        questionToDelete = session.query(questionsSQL).filter_by(questionID=questionID).first()
        if questionToDelete:
            session.delete(questionToDelete)
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def getQuestionByID(questionID: int):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        question = session.query(questionsSQL).filter_by(questionID=questionID).first()
        if question:
            return {
                "questionID": question.questionID,
                "topicID": question.topicID,
                "question": question.question,
                "optionA": question.optionA,
                "optionB": question.optionB,
                "optionC": question.optionC,
                "optionD": question.optionD,
                "answer": question.answer,
                "image": question.image,
                "source": question.source,
            }
        else:
            return None
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()