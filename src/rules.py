from datetime import datetime, timedelta, timezone

class PredictionResult:
    HOME_WIN = "HOME_WIN"
    AWAY_WIN = "AWAY_WIN"
    DRAW = "DRAW"

def is_prediction_locked(kickoff_time_iso: str, buffer_hours: int = 24) -> bool:
    """
    Checks if a game is locked for predictions.
    Logic: Locked if Current Time >= (Kickoff Time - Buffer)
    """
    # Parse the API's ISO date (e.g., '2024-05-19T16:00:00Z')
    kickoff = datetime.fromisoformat(kickoff_time_iso.replace("Z", "+00:00"))
    
    # Get current time in UTC to match API time
    now = datetime.now(timezone.utc)
    
    lock_time = kickoff - timedelta(hours=buffer_hours)
    
    # Return True if we have passed the lock deadline
    return now >= lock_time

def calculate_points_earned(user_pred: str, actual_result: str) -> int:
    """
    Award 1 point for a correct result, 0 for incorrect.
    """
    if not actual_result:
        return 0
        
    return 1 if user_pred.upper() == actual_result.upper() else 0