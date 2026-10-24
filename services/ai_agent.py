import json
from google import genai
from config import settings

class AIAgentEngine:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    async def generate_briefing(self, raw_data: dict) -> str:
        """Generate a daily briefing using Gemini, safely handling missing data keys."""
        emails = raw_data.get('emails', [])
        calendar = raw_data.get('calendar', [])
        fallback_msg = raw_data.get('message', '')

        prompt = f"""
        You are MyAlert, an AI-driven personal assistant running 24/7 in the cloud.
        Generate a concise, professional daily briefing for the user based on the available context below.

        Context:
        - Fallback Status: {fallback_msg}
        - Emails Data: {json.dumps(emails, indent=2)}
        - Calendar Data: {json.dumps(calendar, indent=2)}

        Provide a structured, encouraging briefing with clear headings.
        """

        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
