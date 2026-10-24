from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import traceback
from services.google_client import GoogleDataFetcher
from services.ai_agent import AIAgentEngine
from services.notifier import AudioNotifier

app = FastAPI(title="MyAlert Cloud Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        
        # Bypassed AudioNotifier for cloud Linux container compatibility
        
        return {
            "status": "success",
            "briefing": briefing_markdown
        }
    except Exception as e:
        error_details = traceback.format_exc()
        print("ERROR IN BRIEFING:", error_details)
        return {
            "status": "error",
            "briefing": f"Backend Exception:\n{str(e)}\n\nTraceback:\n{error_details}"
        }
