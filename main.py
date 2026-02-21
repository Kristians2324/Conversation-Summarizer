import sys
import os
from transcriber import transcribe_audio
from summarizer import summarize_text
from drive_uploader import upload_to_drive
from email_sender import send_email
from google_auth import get_creds

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <audio_file_path> <email_address>")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    recipient_email = sys.argv[2]
    
    # Authenticate early to avoid delays later
    print("--- Step 0: Checking Google Authentication ---")
    get_creds()
    
    if not os.path.exists(audio_path):
        print(f"Error: File {audio_path} not found.")
        sys.exit(1)
    
    # 1. Transcribe
    print("--- Step 1: Transcribing Audio ---")
    transcript = transcribe_audio(audio_path)
    if transcript.startswith("Error"):
        print(transcript)
        sys.exit(1)
    
    # 2. Summarize
    print("\n--- Step 2: Summarizing Transcript ---")
    summary = summarize_text(transcript)
    if summary.startswith("Error"):
        print(summary)
        sys.exit(1)
    
    print("\nDraft Summary:")
    print("-" * 20)
    print(summary)
    print("-" * 20)
    
    # 3. Upload to Google Drive
    print("\n--- Step 3: Uploading to Google Drive ---")
    filename = os.path.basename(audio_path).rsplit('.', 1)[0]
    summary_filename = f"{filename}_summary.txt"
    transcript_filename = f"{filename}_transcript.txt"
    
    try:
        upload_to_drive(summary_filename, summary)
        upload_to_drive(transcript_filename, transcript)
        print("Successfully uploaded to Google Drive.")
    except Exception as e:
        print(f"Drive upload failed: {e}")
    
    # 4. Send Email
    print("\n--- Step 4: Sending Email ---")
    subject = f"Conversation Summary: {filename}"
    body = f"Hello,\n\nHere is the summary of your conversation from {filename}:\n\n{summary}\n\nBest regards,\nConversation Summariser Agent"
    
    msg_id = send_email(recipient_email, subject, body)
    if msg_id:
        print(f"Successfully sent email to {recipient_email}. (ID: {msg_id})")
    else:
        print("Failed to send email.")

if __name__ == "__main__":
    main()
