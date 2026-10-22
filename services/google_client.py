import asyncio
import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import settings

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/tasks.readonly'
]

class GoogleDataFetcher:
    def __init__(self):
        self.creds = self._get_credentials()

    def _get_credentials(self):
        creds = None
        if os.path.exists(settings.TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(settings.TOKEN_PATH, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(settings.GOOGLE_CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(settings.TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())
        return creds

    async def fetch_all_context(self):
        """Concurrently fetch Gmail, Calendar, and Tasks data."""
        loop = asyncio.get_running_loop()
        
        emails, calendar_events, tasks = await asyncio.gather(
            loop.run_in_executor(None, self._fetch_emails),
            loop.run_in_executor(None, self._fetch_calendar),
            loop.run_in_executor(None, self._fetch_tasks)
        )
        return {"emails": emails, "calendar": calendar_events, "tasks": tasks}

    def _fetch_emails(self):
        service = build('gmail', 'v1', credentials=self.creds)
        results = service.users().messages().list(userId='me', q='is:unread label:INBOX', maxResults=15).execute()
        messages = results.get('messages', [])
        
        email_data = []
        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['From', 'Subject', 'Date']).execute()
            headers = txt.get('payload', {}).get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            email_data.append({"sender": sender, "subject": subject})
        return email_data

    def _fetch_calendar(self):
        service = build('calendar', 'v3', credentials=self.creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        end_of_day = datetime.datetime.utcnow().replace(hour=23, minute=59, second=59).isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary', timeMin=now, timeMax=end_of_day,
            singleEvents=True, orderBy='startTime').execute()
        return events_result.get('items', [])

    def _fetch_tasks(self):
        service = build('tasks', 'v1', credentials=self.creds)
        tasklists = service.tasklists().list(maxResults=5).execute()
        all_tasks = []
        for tl in tasklists.get('items', []):
            tasks = service.tasks().list(tasklist=tl['id'], showCompleted=False).execute()
            for t in tasks.get('items', []):
                all_tasks.append({"title": t.get('title'), "due": t.get('due')})
        return all_tasks
