from fastapi import FastAPI, HTTPException
import asyncio
from services.google_client import GoogleDataFetcher
from services.ai_agent import AIAgentEngine
from services.notifier import AudioNotifier

app = FastAPI(title="MyAlert Cloud Agent", version="1.0.0")

@app.get("/")
def health_check():
    return {"status": "online", "service": "MyAlert AI Assistant is running 24/7."}

@app.get("/briefing")
async def get_briefing():
    try:
        fetcher = GoogleDataFetcher()
        raw_context = await fetcher.fetch_all_context()
        
        agent = AIAgentEngine()
        briefing_markdown = await agent.generate_briefing(raw_context)
        
        # In cloud mode, play sound locally if supported or log webhook event
        AudioNotifier.play_alert_sound("Glass")
        
        return {
            "status": "success",
            "briefing": briefing_markdown
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
