import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from config import settings

class TimeBlock(BaseModel):
    time_slot: str = Field(description="e.g., 09:00 AM - 10:30 AM")
    activity: str = Field(description="Assigned task or meeting name")
    category: str = Field(description="Deep Work, Admin, Meeting, or Break")

class MorningBriefing(BaseModel):
    executive_summary: str
    urgent_emails: list[str] = Field(description="List of emails requiring immediate attention")
    schedule: list[TimeBlock]

class AIAgentEngine:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    async def generate_briefing(self, raw_data: dict) -> str:
        prompt = f"""
        You are an expert Chief of Staff and productivity engineer. Analyze the following raw daily data:
        
        UNREAD EMAILS:
        {json.dumps(raw_data['emails'], indent=2)}
        
        TODAY'S CALENDAR:
        {json.dumps(raw_data['calendar'], indent=2)}
        
        PENDING TASKS:
        {json.dumps(raw_data['tasks'], indent=2)}
        
        Instructions:
        1. Filter out promotional clutter from emails; flag high-priority items requiring urgent replies.
        2. Intelligently map pending tasks into available gaps between calendar events. Group administrative tasks together and protect large blocks for deep work.
        3. Output a structured executive briefing.
        """

        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=MorningBriefing,
                temperature=0.2,
            ),
        )
        
        parsed_data = json.loads(response.text)
        return self._format_markdown(parsed_data)

    def _format_markdown(self, data: dict) -> str:
        md = f"☀️ **Good Morning! Here is Your Daily Briefing**\n\n"
        md += f"📌 **Executive Summary:**\n{data.get('executive_summary')}\n\n"
        
        urgent = data.get('urgent_emails', [])
        if urgent:
            md += f"🚨 **Urgent Emails ({len(urgent)}):**\n"
            for email in urgent:
                md += f"• {email}\n"
            md += "\n"
            
        md += f"📅 **Optimized Time Blocks:**\n"
        for block in data.get('schedule', []):
            md += f"`{block['time_slot']}` — **{block['activity']}** *({block['category']})*\n"
            
        return md
