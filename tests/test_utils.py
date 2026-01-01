import os
import json

from src.utils import get_team_badge

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

def test_get_team_badge():
    json_path = os.path.join(project_root, "mock", "mock_matches.json")

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Could not find mock_matches.json at: {json_path}")

    with open(json_path, 'r') as f:
        data = json.load(f)
        matches = data.get("matches", [])
    first_match = matches[0]

    #assert get_team_badge(match=first_match, team="HOME")== "https://crests.football-data.org/64.png"
    assert get_team_badge(match=first_match, team="AWAY")== "https://crests.football-data.org/bournemouth.png"