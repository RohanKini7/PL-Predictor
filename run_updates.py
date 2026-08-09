import os
from datetime import datetime
import pytz

# Import your existing functions
from dataset.update_supabase import update_fixtures_from_json
from dataset.api_client import fetch_pl_fixtures

def main():
    print("--- Starting Hourly Update ---")

    # 1. Fetch data from Football API and save to JSON
    print("Step 1: Fetching API data...")
    fetch_pl_fixtures()

    # 2. Push that JSON data to Supabase
    print("Step 2: Updating Supabase tables...")
    update_fixtures_from_json()

    # 3. Write the .txt log file
    print("Step 3: Writing timestamp...")
    german_tz = pytz.timezone('Europe/Berlin')
    now = datetime.now(german_tz)
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")

    with open("last_sync.txt", "w") as f:
        f.write(f"Database last synchronized: {timestamp_str} (CET)")

    print(f"--- Update Complete at {timestamp_str} ---")


if __name__ == "__main__":
    main()