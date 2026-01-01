import subprocess
import json
import os
import sys
import streamlit as st
from supabase import create_client, Client
current_dir = os.path.dirname(os.path.abspath(__file__))

from dotenv import load_dotenv

load_dotenv()

def fetch_pl_fixtures():
    # This is the exact command that worked for you in the terminal
    token = st.secrets("FOOTBALL_API_KEY")
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
            print(f"Curl Error: {result.stderr}")
            return []
        filename = os.path.join(current_dir, "pl_season_data.json")
        # Convert the text result into a Python dictionary
        data = json.loads(result.stdout)
        with open(filename, "w", encoding="utf-8") as f:
            # indent=4 makes the file human-readable (pretty-print)
            json.dump(data, f, indent=4)
            print("Done")
        
    except Exception as e:
        print(f"Failed to run curl from Python: {e}")
        return []
    
if __name__ == "__main__":
    fetch_pl_fixtures()