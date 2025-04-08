import json
from dotenv import load_dotenv
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


load_dotenv()
credentials_file = os.getenv("GOOGLE_API_TOKEN")
credentials_info = json.loads(credentials_file)

credentials = service_account.Credentials.from_service_account_info(
    credentials_info,
    scopes=['https://www.googleapis.com/auth/drive']
)

drive_service = build('drive', 'v3', credentials=credentials)
parent_folder_id = '1m3wrlAi01sdKag3a5QMXfIT36cafDnaM'
def get_folders_in_folder(folder_id=parent_folder_id):
    folders_dict = {}

    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder'",
        fields="files(id, name)"
    ).execute()

    folders = results.get('files', [])

    for folder in folders:
        folder_name = folder['name']
        folder_id = folder['id']
        folders_dict[folder_name] = folder_id

    return folders_dict



def uploadQuestionImage(topicID,questionID,imagePath):
    folder_id = get_folders_in_folder()[topicID]
    file_metadata = {'name': str(questionID), 'parents': [folder_id]}
    media = MediaFileUpload(imagePath, resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    try:
        os.remove(imagePath)
    except:
        pass
    return f'https://drive.google.com/file/d/{file["id"]}'

def deleteImage(topicID,questionID):
    folder_id = get_folders_in_folder()[topicID]
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and name='{questionID}'",
        fields="files(id)"
    ).execute()

    files = results.get('files', [])
    if len(files) > 0:
        file_id = files[0]['id']
        drive_service.files().delete(fileId=file_id).execute()
        return True
    else:
        return False

def createFolder(topicID):
    file_metadata = {
        'name': topicID,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id]
    }
    file = drive_service.files().create(body=file_metadata, fields='id').execute()
    return file.get('id')