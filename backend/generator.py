from uuid import uuid4
import secrets
import string
import random
userID = "user-"+str(uuid4())
sessionToken = "session-"+str(uuid4())
def generateRecoveryCode():
    return ''.join(secrets.choice(string.ascii_uppercase) for _ in range(4))
recoveryCode = str([generateRecoveryCode() for _ in range(8)])

def generateSessionToken():
    return "session-"+str(uuid4())

def generateTempFileName():
    return str(uuid4())+".jpg"

def generateRamdomSixComments(comments):
    if len(comments) > 6:
        comments = random.sample(comments, 6)
    else:
        comments = random.sample(comments, len(comments))
    return comments