from src.api_client import fetch_pl_fixtures
from supabase import create_client
import os

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def sync():
    matches = fetch_pl_fixtures()
    print(f"🔄 Syncing {len(matches)} matches...")
    exit()

    for m in matches:
        # Prepare the row for Supabase
        row = {
            "fixture_id": m['id'],
            "home_team": m['homeTeam']['name'],
            "away_team": m['awayTeam']['name'],
            "kickoff_time": m['utcDate'],
            "status": m['status']
        }
        
        # Calculate score ONLY if the match is finished
        if m['status'] == 'FINISHED':
            h_score = m['score']['fullTime']['home']
            a_score = m['score']['fullTime']['away']
            
            if h_score > a_score: row["final_score"] = "HOME_WIN"
            elif a_score > h_score: row["final_score"] = "AWAY_WIN"
            else: row["final_score"] = "DRAW"

        supabase.table("fixtures").upsert(row).execute()

    print("✅ 2025/26 Season Synced!")

if __name__ == "__main__":
    sync()