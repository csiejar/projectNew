from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .dbClass import *
# from dbClass import *
from fastapi import HTTPException
import generator
import ast
import random
import datetime


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
                "userImg": user.userImg,
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
def createUser(googleID, name, email,userImg):
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
            sex=0, # 不願透露-0 男-1 女-2
            userImg=userImg
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
                "sex": user.sex,
                "userImg": user.userImg
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
                return "True"
            else:
                return question.answer
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

def getSixComments():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        comments = session.query(commentsSQL).all()
        user = session.query(UsersSQL).all()
        question = session.query(questionsSQL).all()
        # 將資料轉換為字典格式
        comments = [
            {
                "userID": comment.userID,
                "comment": comment.comment,
                "userName": next((u.name for u in user if u.userID == comment.userID), None),
                "questionID": comment.questionID,
                "question": next((q.question for q in question if q.questionID == comment.questionID), None),
                "userImg": next((u.userImg for u in user if u.userID == comment.userID), None),
            }
            for comment in comments
        ]
        comments = generator.generateRamdomSixComments(comments)
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

def getAllPermission():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        permission = session.query(permissionSQL).all()
        # 將資料轉換為字典格式
        permission = [
            {
                "permissionID": permission.permissionID,
                "permissionDetails": permission.permissionDetails,
                "allowLink": permission.allowLink,
                "permissionUser": permission.permissionUser
            }
            for permission in permission
        ]
        return permission
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def getUserPermission(userID):
    permissionList = []
    for i in getAllPermission():
        if userID in i['permissionUser']:
            permissionList.append(i['permissionID'])
    return permissionList

def isUserAllowToAccessLink(userID, link):
    permissionList = getUserPermission(userID)
    for i in permissionList:
        permission = getAllPermission()
        for j in permission:
            if i == j['permissionID'] and link in j['allowLink']:
                return True
    return False

def getUserNameByID(userID):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(UsersSQL).filter_by(userID=userID).first()
        if user:
            return user.name
        else:
            return "unknown"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def getAllPermissionDetails():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        permission = session.query(permissionSQL).all()
        # 將資料轉換為字典格式
        permission = [
            {
                "permissionID": permission.permissionID,
                "permissionDetails": permission.permissionDetails,
                "allowLink": ast.literal_eval(permission.allowLink),
                "permissionUser": ast.literal_eval(permission.permissionUser),
                "permissionUserName": [getUserNameByID(userID) for userID in ast.literal_eval(permission.permissionUser)]
            }
            for permission in permission
        ]
        return permission
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def getAllUsersIDAndName():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        users = session.query(UsersSQL).all()
        # 將資料轉換為字典格式
        users = [
            {
                "userID": user.userID,
                "userName": user.name,
            }
            for user in users
        ]
        return users
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def addUserToPermission(permissionID, userID):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        permission = session.query(permissionSQL).filter_by(permissionID=permissionID).first()
        if permission:
            if userID in ast.literal_eval(permission.permissionUser):
                return "用戶已有權限"
            # 將 permissionUser 轉換為列表，並添加新的 userID
            permission.permissionUser = str(ast.literal_eval(permission.permissionUser) + [userID])
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def getQuestionsForQuestionPage(): # 取得所有題目（無答案）
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        questions = session.query(questionsSQL).all()
        random.shuffle(questions)
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


def submitQuestionAnswer(usersAnswer:dict):
    returnData = []
    wrongAnswer = {}
    for i in usersAnswer.keys():
        if checkAnswer(i, usersAnswer[i]) != "True":
            wrongAnswer[i] = checkAnswer(i, usersAnswer[i])
    returnData = [usersAnswer, wrongAnswer]
    return returnData

def uploadUsersAnswer(userID, usersAnswer:dict):
    usersAnswer = submitQuestionAnswer(usersAnswer)
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        recordID = 0
        lastUploadID = session.query(answerRecordsSQL).order_by(answerRecordsSQL.recordID.desc()).first()
        if lastUploadID:
            recordID = lastUploadID.recordID + 1
        new_upload = answerRecordsSQL(
            recordID=recordID,
            userID=userID,
            answers=str(usersAnswer),
            timestamp=datetime.datetime.now()
        )
        session.add(new_upload)
        session.commit()
        return recordID
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def getAnswerRecord(recordID):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        record = session.query(answerRecordsSQL).filter_by(recordID=recordID).first()
        if record:
            return {
                "recordID": record.recordID,
                "userID": record.userID,
                "originalAnswers": ast.literal_eval(record.answers)[0],
                "checkedAnswers": ast.literal_eval(record.answers)[1],
                "timestamp": str(record.timestamp)
            }
        else:
            return None
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def getQuestionsForAnswerRecord(recordID):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        record = session.query(answerRecordsSQL).filter_by(recordID=recordID).first()
        returnData = []
        if record:
            answeredQuestionNumber = ast.literal_eval(record.answers)[0].keys()
            for i in answeredQuestionNumber:
                question = session.query(questionsSQL).filter_by(questionID=i).first()
                if question:
                        returnData.append({
                            "questionID": question.questionID,
                            "topicID": question.topicID,
                            "question": question.question,
                            "optionA": question.optionA,
                            "optionB": question.optionB,
                            "optionC": question.optionC,
                            "optionD": question.optionD,
                            "image": question.image,
                            "source": question.source,
                            })
            return returnData
        else:
            return None
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def getUserAnswerRecord(userID):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        records = session.query(answerRecordsSQL).filter_by(userID=userID).all()
        # 將資料轉換為字典格式
        records = [
            {
                "recordID": record.recordID,
                "timestamp": str(record.timestamp),
                "correctAnswersCount": len(ast.literal_eval(record.answers)[0]) - len(ast.literal_eval(record.answers)[1]),
                "totalAnswersCount": len(ast.literal_eval(record.answers)[0])
            }
            for record in records
        ]
        records.reverse()
        return records
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def isUsersRecord(userID,recordID):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        record = session.query(answerRecordsSQL).filter_by(recordID=recordID).first()
        if record:
            if record.userID == userID:
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def getUsersAnswer(recordID):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        record = session.query(answerRecordsSQL).filter_by(recordID=recordID).first()
        if record:
            return ast.literal_eval(record.answers)
        else:
            return None
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def getQuestionsTopicID(questionID):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        question = session.query(questionsSQL).filter_by(questionID=questionID).first()
        if question:
            return question.topicID
        else:
            return None
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def writeUserTopicStats(userID, uploadData):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(UsersSQL).filter_by(userID=userID).first()
        if user:
            user.topic_stats = str(uploadData)
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        return f"Error: {str(e)}"

def getUserTopicStats(userID):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(UsersSQL).filter_by(userID=userID).first()
        if user:
            return ast.literal_eval(user.topic_stats)
        else:
            return None
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def getUserTopicsCorrectRate(userID):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        topics = session.query(topicsSQL).all()
        topicWithQuestionID = {}
        userRecords = getUserAnswerRecord(userID)
        topicCorrectQuestionsCount = {}
        topicAnsweredQuestionsCount = {}
        questionIDAndTopicID = {}
        lastRecordID = 0
        pastRecords = (session.query(UsersSQL).filter_by(userID=userID).first()).topic_stats
        if pastRecords:
            pastRecords = ast.literal_eval(pastRecords)
            lastRecordID = pastRecords[3] # 取得上次答對率算到哪了
        newestRecordID = 0
        if userRecords:
            newestRecordID = userRecords[0]['recordID']

        if lastRecordID == newestRecordID:
            return pastRecords
            
        if lastRecordID == 0:
            for topic in topics:
                topicID = topic.topicID
                totalQuestions = session.query(questionsSQL).filter_by(topicID=topicID).all()
                questionIDs = []
                for i in totalQuestions:
                    if i.questionID not in questionIDs:
                        questionIDs.append(i.questionID)
                topicWithQuestionID[topicID] = questionIDs # 每個單元的題目ID列表

            for record in userRecords:
                usersAnswer = getUsersAnswer(record['recordID'])
                questionIDs = list(usersAnswer[0].keys())
                for questionID in questionIDs:
                    topicID = getQuestionsTopicID(questionID)
                    if topicID not in questionIDAndTopicID:
                        questionIDAndTopicID[questionID] = topicID
                correctQuestionsID = []
                for answers in usersAnswer[0].keys():
                    if answers not in usersAnswer[1].keys():
                        correctQuestionsID.append(answers)
                wrongQuestionsID = []
                for i in usersAnswer[1].keys():
                    wrongQuestionsID.append(i)
                totalQuestionsID = list(usersAnswer[0].keys())
            
                for i in totalQuestionsID:
                    topicID = questionIDAndTopicID[i]
                    if topicID not in topicAnsweredQuestionsCount:
                        topicAnsweredQuestionsCount[topicID] = 0
                    topicAnsweredQuestionsCount[topicID] += 1
                for i in correctQuestionsID:
                    topicID = questionIDAndTopicID[i]
                    if topicID not in topicCorrectQuestionsCount:
                        topicCorrectQuestionsCount[topicID] = 0
                    topicCorrectQuestionsCount[topicID] += 1
            userTopicsCorrectRate = {}
            for topicID in topicWithQuestionID.keys():
                if topicID not in topicCorrectQuestionsCount:
                    topicCorrectQuestionsCount[topicID] = 0
                if topicID not in topicAnsweredQuestionsCount:
                    topicAnsweredQuestionsCount[topicID] = 0
                if topicAnsweredQuestionsCount[topicID] == 0:
                    userTopicsCorrectRate[topicID] = 0
                else:
                    userTopicsCorrectRate[topicID] = round((topicCorrectQuestionsCount[topicID] / topicAnsweredQuestionsCount[topicID]) * 100,2)

            writeUserTopicStats(userID, [userTopicsCorrectRate, topicCorrectQuestionsCount, topicAnsweredQuestionsCount, newestRecordID])
            return [userTopicsCorrectRate, topicCorrectQuestionsCount, topicAnsweredQuestionsCount, newestRecordID]
        if lastRecordID != 0 and lastRecordID < newestRecordID:
            for topic in topics:
                topicID = topic.topicID
                totalQuestions = session.query(questionsSQL).filter_by(topicID=topicID).all()
                questionIDs = []
                for i in totalQuestions:
                    if i.questionID not in questionIDs:
                        questionIDs.append(i.questionID)
                topicWithQuestionID[topicID] = questionIDs
            for record in userRecords:
                if record['recordID'] <= lastRecordID:
                    continue
                usersAnswer = getUsersAnswer(record['recordID'])
                questionIDs = list(usersAnswer[0].keys())
                for questionID in questionIDs:
                    topicID = getQuestionsTopicID(questionID)
                    if topicID not in questionIDAndTopicID:
                        questionIDAndTopicID[questionID] = topicID
                correctQuestionsID = []
                for answers in usersAnswer[0].keys():
                    if answers not in usersAnswer[1].keys():
                        correctQuestionsID.append(answers)
                wrongQuestionsID = []
                for i in usersAnswer[1].keys():
                    wrongQuestionsID.append(i)
                totalQuestionsID = list(usersAnswer[0].keys())
            
                for i in totalQuestionsID:
                    topicID = questionIDAndTopicID[i]
                    if topicID not in topicAnsweredQuestionsCount:
                        topicAnsweredQuestionsCount[topicID] = 0
                    topicAnsweredQuestionsCount[topicID] += 1
                for i in correctQuestionsID:
                    topicID = questionIDAndTopicID[i]
                    if topicID not in topicCorrectQuestionsCount:
                        topicCorrectQuestionsCount[topicID] = 0
                    topicCorrectQuestionsCount[topicID] += 1
            userTopicsCorrectRate = {}
            for topicID in topicWithQuestionID.keys():
                if topicID not in topicCorrectQuestionsCount:
                    topicCorrectQuestionsCount[topicID] = 0
                if topicID not in topicAnsweredQuestionsCount:
                    topicAnsweredQuestionsCount[topicID] = 0
                if topicAnsweredQuestionsCount[topicID] == 0:
                    userTopicsCorrectRate[topicID] = 0
                else:
                    userTopicsCorrectRate[topicID] = round((topicCorrectQuestionsCount[topicID] / topicAnsweredQuestionsCount[topicID]) * 100,2)
            # 原本累積資料（從資料庫撈出來）
                originalUserTopicsCorrectRate = getUserTopicStats(userID)[0]
                originalTopicCorrectQuestionsCount = getUserTopicStats(userID)[1]
                originalTopicAnsweredQuestionsCount = getUserTopicStats(userID)[2]

                # 累加後的新資料
                mergedCorrectCount = {}
                mergedAnsweredCount = {}
                mergedCorrectRate = {}

                for topicID in topicWithQuestionID.keys():
                    originalCorrect = originalTopicCorrectQuestionsCount.get(topicID, 0)
                    originalAnswered = originalTopicAnsweredQuestionsCount.get(topicID, 0)
                    newCorrect = topicCorrectQuestionsCount.get(topicID, 0)
                    newAnswered = topicAnsweredQuestionsCount.get(topicID, 0)

                    mergedCorrectCount[topicID] = originalCorrect + newCorrect
                    mergedAnsweredCount[topicID] = originalAnswered + newAnswered

                    if mergedAnsweredCount[topicID] == 0:
                        mergedCorrectRate[topicID] = 0
                    else:
                        mergedCorrectRate[topicID] = round((mergedCorrectCount[topicID] / mergedAnsweredCount[topicID]) * 100, 2)

                # 寫回資料庫
                writeUserTopicStats(userID, [mergedCorrectRate, mergedCorrectCount, mergedAnsweredCount, newestRecordID])
                return [mergedCorrectRate, mergedCorrectCount, mergedAnsweredCount, newestRecordID]
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def getAllTopicsTitleWithID():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        topics = session.query(topicsSQL).all()
        # 將資料轉換為字典格式
        topics = [
            {
                "topicID": topic.topicID,
                "title": ''.join(char for char in topic.title if not char.isdigit()).replace('.', '').replace('-','').replace('YΔ','Y-Δ').strip()
            }
            for topic in topics
        ]
        return topics
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()
    
def getSelectedQuestion(topicIDs:list, questionCount:int):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        questions = session.query(questionsSQL).filter(questionsSQL.topicID.in_(topicIDs)).all()
        if len(questions) < questionCount:
            return "Error: 選擇的題目數量超過可用題目數量"
        selectedQuestions = random.sample(questions, questionCount)
        # 將資料轉換為字典格式
        selectedQuestions = [
            {
                "questionID": question.questionID,
                "topicID": question.topicID,
                "question": question.question,
                "optionA": question.optionA,
                "optionB": question.optionB,
                "optionC": question.optionC,
                "optionD": question.optionD,
                "image": question.image,
                "source": question.source,
            }
            for question in selectedQuestions
        ]
        return selectedQuestions
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        session.close()

def getTopicsForQuestionSelector():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        topics = session.query(topicsSQL).all()
        # 將資料轉換為字典格式
        topics = [
            {
                "topicID": topic.topicID,
                "paragraph": topic.title.split(" ")[0].split("-")[0],  # 擷取段落名（如有空白或 dash）
                "title": ''.join(char for char in topic.title if not char.isdigit()) \
                            .replace('.', '').replace('-', '').replace('YΔ', 'Y-Δ').strip(),
                "quesitonCount": session.query(questionsSQL).filter_by(topicID=topic.topicID).count(),
            }
            for topic in topics
        ]
        return topics
    except Exception as e:
        return {"error": str(e)}
    finally:
        session.close()

