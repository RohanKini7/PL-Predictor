from datetime import datetime, timedelta, timezone

def get_mock_pl_fixtures():
    """Generates fake PL fixtures to test your UI and Logic."""
    now = datetime.now(timezone.utc)
    
    return [
        {
            "fixture": {
                "id": 99901,
                "match_day": 1,
                "date": (now + timedelta(hours=48)).isoformat(), # Open: 2 days away
                "status": {"short": "NS"}
            },
            "teams": {
                "home": {"name": "Arsenal"},
                "away": {"name": "Liverpool"}
            },
            "goals": {"home": None, "away": None}
        },
        {
            "fixture": {
                "id": 99902,
                "match_day": 2,
                "date": (now + timedelta(hours=10)).isoformat(), # Locked: 10 hours away
                "status": {"short": "NS"}
            },
            "teams": {
                "home": {"name": "Man City"},
                "away": {"name": "Chelsea"}
            },
            "goals": {"home": None, "away": None}
        }
    ]