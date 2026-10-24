import os
from config import settings

class GoogleDataFetcher:
    def __init__(self):
        self.credentials_path = settings.GOOGLE_CREDENTIALS_PATH
        self.token_path = settings.TOKEN_PATH

    async def fetch_all_context(self) -> dict:
        """Fetch context safely, falling back if running in the cloud without local OAuth credentials."""
        if not os.path.exists(self.credentials_path) or not os.path.exists(self.token_path):
            print("Warning: Google OAuth credentials not found in cloud environment. Using cloud fallback context.")
            return {
                "source": "Cloud Fallback",
                "message": "MyAlert is running 24/7 in the cloud. Local OAuth desktop files (credentials.json) are not present, operating in cloud-safe mode."
            }
        
        try:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request
            
            creds = None
            if os.path.exists(self.token_path):
                creds = Credentials.from_authorized_user_file(
                    self.token_path, 
                    ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/calendar.readonly']
                )
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    return {
                        "source": "Cloud Fallback",
                        "message": "OAuth token is invalid or expired."
                    }
            
            return {
                "source": "Google API",
                "status": "Authenticated successfully"
            }
        except Exception as e:
            print(f"OAuth load error: {e}")
            return {"source": "Error fallback", "details": str(e)}
