import dotenv
import os
dotenv.load_dotenv()

from paramiko import SSHClient, AutoAddPolicy

client = SSHClient()
client.set_missing_host_key_policy(AutoAddPolicy())  # 加上這行

sshUsername = os.getenv('SSHUSERNAME')
sshPassword = os.getenv('SSHPASSWORD')
sshIp = os.getenv('SSHIP')
# 本地與遠端路徑
local_path = 'imgTest.png'
remote_path = 'C:\\Users\\Ga\\Desktop\\projectNew\\img\\imgTest.png'

try:
    # 建立 SSH 連線
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(sshIp, username=sshUsername, password=sshPassword)
    # client.exec_command("cd C:\\Users\\Ga\\Desktop\\projectNew && mkdir img") #建立 img 資料夾
    client.exec_command(f"cd C:\\Users\\Ga\\Desktop\\projectNew && mkdir img") #建立 img 資料夾+以topicID建立子資料夾
    client.exec_command(f"cd C:\\Users\\Ga\\Desktop\\projectNew\\img && mkdir {26}") #建立 img 資料夾+以topicID建立子資料夾

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

except Exception as e:
    print(f"上傳失敗: {e}")