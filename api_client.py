import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_pl_fixtures():
    """Fetches all Premier League fixtures for the 2024 season."""
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    
    headers = {
        "X-RapidAPI-Key": os.getenv("FOOTBALL_API_KEY"),
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    
    # League 39 is Premier League, Season 2024
    params = {"league": "39", "season": "2021"}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() # Check for errors
        print("✅ API Request Successful")
        return response.json().get("response", [])
    except Exception as e:
        print(f"❌ API Error: {e}")
        return []
if __name__ == "__main__":
    fixtures = fetch_pl_fixtures()
    for fixture in fixtures:
        print(fixture)