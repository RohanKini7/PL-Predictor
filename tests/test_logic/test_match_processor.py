import sys
import os
import json
from datetime import datetime, timezone

current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the project root (one level up from 'tests')
project_root = os.path.dirname(current_dir)

# Add project root to sys.path if it's not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.logic.match_processor import process_fixtures, is_match_locked

def test_with_real_json_file():
    print("📋 Testing: Loading real data from mock_matches.json...")
    
    # Path to your json file
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mock', 'mock_matches.json'))
    
    if not os.path.exists(json_path):
        print(f"⚠️  Skipping test: {json_path} not found.")
        return

    with open(json_path, 'r') as f:
        data = json.load(f)
        matches = data.get("matches", [])

    # 1. Test Grouping
    grouped, current_md = process_fixtures(matches)
    
    assert len(matches) > 0, "JSON file should contain matches"
    assert len(grouped) > 0, "Matches should be grouped into matchdays"
    assert current_md is not None, "There should be a current active matchday"

    # 2. Test a specific match from the JSON
    first_match = matches[0]
    locked = is_match_locked(first_match['utcDate'])
    assert locked is not None, "Lock status should be determined"
    

def test_grouping_logic():
    print("📋 Testing: Manual Matchday Grouping...")
    mock_data = [
        {"matchday": 1, "status": "FINISHED"},
        {"matchday": 1, "status": "FINISHED"},
        {"matchday": 2, "status": "TIMED"},
    ]
    grouped, _ = process_fixtures(mock_data)
    assert len(grouped) == 2


def test_current_matchday_detection():
    print("📋 Testing: Current Matchday Detection...")
    mock_data = [
        {"matchday": 18, "status": "FINISHED"},
        {"matchday": 19, "status": "TIMED"}, # Active
    ]
    _, current_md = process_fixtures(mock_data)
    assert current_md == 19

if __name__ == "__main__":
    test_with_real_json_file()
    test_grouping_logic()
    test_current_matchday_detection()
    print("✅ All tests passed!")