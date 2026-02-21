import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth import get_creds

def send_email(to, subject, body):
    """Sends an email using the Gmail API."""
    creds = get_creds()
    service = build('gmail', 'v1', credentials=creds)
    
    # Create the message
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    
    # Encode the message in base64
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    
    try:
        sent_message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        return sent_message.get('id')
    except Exception as e:
        print(f"Failed to send email: {e}")
        return None
