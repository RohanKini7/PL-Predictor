import subprocess
import os
import json
from dotenv import load_dotenv


load_dotenv()

def save_mock_data():
    token = os.getenv("FOOTBALL_API_KEY")
    command = [
        "curl", "-s", "-X", "GET", 
        "https://api.football-data.org/v4/competitions/PL/matches",
        "-H", f"X-Auth-Token: {token}",
        "-H", "X-Unfold-Goals: true"
    ]
    
    print("📡 Fetching real data to create mock file...")
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        data = json.loads(result.stdout)
        with open("mock/mock_matches.json", "w") as f:
            json.dump(data, f, indent=4)
    else:
        print({result.stderr})

if __name__ == "__main__":
    save_mock_data()