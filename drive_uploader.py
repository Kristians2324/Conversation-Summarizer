import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google_auth import get_creds

def upload_to_drive(filename, content, mime_type="text/plain", folder_name="Summaries"):
    """Uploads content to a specific folder in Google Drive."""
    creds = get_creds()
    service = build('drive', 'v3', credentials=creds)
    
    # 1. Find or create the folder
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    
    if items:
        folder_id = items[0]['id']
    else:
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')
    
    # 2. Upload the file
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    
    media = MediaIoBaseUpload(io.BytesIO(content.encode('utf-8') if isinstance(content, str) else content), 
                              mimetype=mime_type)
    
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')
