from src.rules import is_prediction_locked, calculate_points_earned
from datetime import datetime, timedelta, timezone

def test_24h_lock_logic():
    # Set a fake kickoff 25 hours from now (Should NOT be locked)
    future_kickoff = (datetime.now(timezone.utc) + timedelta(hours=25)).isoformat()
    assert is_prediction_locked(future_kickoff) == False
    
    # Set a fake kickoff 10 hours from now (Should BE locked)
    soon_kickoff = (datetime.now(timezone.utc) + timedelta(hours=10)).isoformat()
    assert is_prediction_locked(soon_kickoff) == True

def test_scoring():
    assert calculate_points_earned("HOME_WIN", "HOME_WIN") == 1
    assert calculate_points_earned("DRAW", "AWAY_WIN") == 0

    