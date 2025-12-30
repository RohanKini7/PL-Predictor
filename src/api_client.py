import subprocess
import json
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_pl_fixtures():
    # This is the exact command that worked for you in the terminal
    token = os.getenv("FOOTBALL_API_KEY")
    command = [
        "curl", 
        "-X", "GET", 
        "https://api.football-data.org/v4/competitions/PL/matches",
        "-H", f"X-Auth-Token: {token}",
        "-H", "X-Unfold-Goals: true"
    ]
    
    try:
        # We run the command and capture the text it prints out
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Curl Error: {result.stderr}")
            return []
            
        # Convert the text result into a Python dictionary
        data = json.loads(result.stdout)
        return data.get("matches", [])
        
    except Exception as e:
        print(f"❌ Failed to run curl from Python: {e}")
        return []
    
if __name__ == "__main__":
    fixtures = fetch_pl_fixtures()
    for fixture in fixtures:
        print(fixture)