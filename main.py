import asyncio
from services.google_client import GoogleDataFetcher
from services.ai_agent import AIAgentEngine
from services.notifier import AudioNotifier

async def main():
    print("🚀 Initializing MyAlert Agent...")
    fetcher = GoogleDataFetcher()
    
    print("📥 Fetching data from Google APIs...")
    raw_context = await fetcher.fetch_all_context()
    
    print("🧠 Generating AI Briefing and Time-Blocking Schedule...")
    agent = AIAgentEngine()
    briefing_markdown = await agent.generate_briefing(raw_context)
    
    # Play success ringtone alert
    AudioNotifier.play_alert_sound("Glass")
    
    print("\n" + "="*50 + "\n")
    print(briefing_markdown)
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
