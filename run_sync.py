import os
from dotenv import load_dotenv
from supabase import create_client
from src.mock_api import get_mock_pl_fixtures # Import mock instead of real API

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def sync_mock_data():
    print("🧪 Syncing Mock Data for testing...")
    data = get_mock_pl_fixtures()
    
    for item in data:
        f = item['fixture']
        t = item['teams']
        
        match_data = {
            "fixture_id": f['id'],
            "matchday": f['match_day'],
            "kickoff_time": f['date'],
            "home_team": t['home']['name'],
            "away_team": t['away']['name'],
            "status": f['status']['short'],
            "final_score": None
        }
        supabase.table("mock_fixtures").upsert(match_data).execute()
    
    print("✅ Mock fixtures uploaded to Supabase!")

if __name__ == "__main__":
    sync_mock_data()