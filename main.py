import asyncio
from services.google_client import GoogleDataFetcher
from services.ai_agent import AIAgentEngine
from services.notifier import TelegramNotifier

async def main():
    print("🚀 Initializing MyAlert Agent...")
    
    fetcher = GoogleDataFetcher()
    agent = AIAgentEngine()
    notifier = TelegramNotifier()
    
    print("📥 Fetching data from Google APIs...")
    raw_context = await fetcher.fetch_all_context()
    
    print("🧠 Generating AI Briefing and Time-Blocking Schedule...")
    briefing_markdown = await agent.generate_briefing(raw_context)
    
    print("📤 Dispatching notification...")
    await notifier.send_message(briefing_markdown)
    print("✅ Morning briefing sent successfully!")

if __name__ == "__main__":
    asyncio.run(main())
