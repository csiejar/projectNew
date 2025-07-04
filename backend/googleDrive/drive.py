# import json
from dotenv import load_dotenv
import os
from paramiko import SSHClient, AutoAddPolicy
client = SSHClient()
client.set_missing_host_key_policy(AutoAddPolicy())  # 加上這行
load_dotenv()

sshUsername = os.getenv('SSHUSERNAME')
sshPassword = os.getenv('SSHPASSWORD')
sshIp = os.getenv('SSHIP')

def uploadQuestionImage(topicID,questionID,imagePath):
    local_path = imagePath
    remote_path = f'C:\\Users\\Ga\\Desktop\\projectNew\\img\\{topicID}\\{questionID}.png'
    print(f"local_path: {local_path}")
    print(f"remote_path: {remote_path}")


    try:
        # 建立 SSH 連線
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(sshIp, username=sshUsername, password=sshPassword)
        client.exec_command(f"cd C:\\Users\\Ga\\Desktop\\projectNew && mkdir img") #建立 img 資料夾+以topicID建立子資料夾
        client.exec_command(f"cd C:\\Users\\Ga\\Desktop\\projectNew\\img && mkdir {topicID}") #建立 img 資料夾+以topicID建立子資料夾
        # 建立 SFTP 連線
        sftp = client.open_sftp()

        # 轉換 Windows 路徑為 SFTP 可接受格式（把 C:\ 換成 /C:/）
        remote_path_sftp = remote_path.replace('\\', '/')
        if remote_path_sftp[1:3] == ':/':
            remote_path_sftp = '/' + remote_path_sftp
        # 上傳檔案
        sftp.put(local_path, remote_path_sftp)

        print(f"成功上傳 {local_path} 到遠端 {remote_path_sftp}")

        sftp.close()
        client.close()
        return {"status": "success", "message": f"成功上傳 {local_path} 到遠端 {remote_path_sftp}"}

    except Exception as e:
        print(f"上傳失敗: {e}")
        return {"status": "error", "message": str(e)}