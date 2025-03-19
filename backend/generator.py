from uuid import uuid4
import secrets
import string
userID = "user-"+str(uuid4())
sessionToken = "session-"+str(uuid4())
def generate_code():
    return ''.join(secrets.choice(string.ascii_uppercase) for _ in range(4))
recoveryCode = str([generate_code() for _ in range(8)])