import sys
import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from match_processor import process_fixtures, is_match_locked

def test_with_real_json_file():
    json_path = os.path.join(project_root, "..", "dataset", "mock_matches.json")
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Could not find pl_season_data.json at: {json_path}")

    with open(json_path, 'r') as f:
        data = json.load(f)
        matches = data.get("matches", [])

    # 1. Test Grouping
    grouped, current_md = process_fixtures(matches)
    
    assert len(matches) == 380
    assert len(grouped) == 38, "Matches should be grouped into matchdays"
    assert current_md is not None, "There should be a current active matchday"

    # 2. Test a specific match from the JSON
    first_match = matches[0]
    locked = is_match_locked(first_match['utcDate'])
    assert locked is True

    # 3. Last Match should not be locked [valid only before the season ends]
    last_match = matches[-1]
    locked = is_match_locked(last_match['utcDate'])
    assert locked is False


def test_grouping_logic():
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
