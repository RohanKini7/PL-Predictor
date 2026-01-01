import json
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Initialize Supabase Client
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")  # Use service role for write access
supabase: Client = create_client(url, key)


def update_fixtures_from_json():
    # 1. Load your dataset JSON file
    with open("dataset/pl_season_data.json", "r") as f:
        data = json.load(f)

    matches = data.get("matches", [])
    print(f"Processing {len(matches)} matches...")

    formatted_matches = []

    for match in matches:
        # Determine the winner/status for your 'final_score' logic
        # Based on your setup, final_score stores HOME_WIN, AWAY_WIN, or DRAW
        winner = match.get('score', {}).get('winner')

        # Mapping the JSON match to your DB schema
        fixture_item = {
            "fixture_id": match['id'],  #
            "matchday": match['matchday'],  #
            "kickoff_time": match['utcDate'],  #
            "home_team": match['homeTeam']['shortName'],  #
            "away_team": match['awayTeam']['shortName'],  #
            "status": match['status'],  #
            "final_score": winner if winner else "PENDING",  #
            "crest_home": match['homeTeam'].get('crest'),  #
            "crest_away": match['awayTeam'].get('crest'),  #
        }
        formatted_matches.append(fixture_item)

    # 2. Upsert to Supabase
    # on_conflict handles updating existing IDs instead of failing
    try:
        supabase.table("mock_fixtures").upsert(
            formatted_matches,
            on_conflict="fixture_id"
        ).execute()
        print(f"Successfully updated {len(formatted_matches)} rows.")
    except Exception as e:
        print(f"Error updating Supabase: {e}")


if __name__ == "__main__":
    update_fixtures_from_json()