from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def run():
    credentials = service_account.Credentials.from_service_account_file(
        '/home/hoseung2/dfmba-img-trading-302b9a5ad821.json',
        scopes=['https://www.googleapis.com/auth/drive']
    )
    
    drive_service = build('drive', 'v3', credentials=credentials)
    local_file_path = '/locdisk/data/hoseung2/img/compresstogdrive.tar.gz'
    
    file_metadata = {
        'name': 'market_total.tar.gz',
        'parents': ['']
    }
    
    media = MediaFileUpload(local_file_path, mimetype='text/plain')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
    print(f'File ID: {file["id"]}')

if __name__ == '__main__':
    run()
