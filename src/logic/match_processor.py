from datetime import datetime, timedelta, timezone

def process_fixtures(fixtures):
    """
    Groups fixtures by matchday and finds the current active matchday.
    Returns: (grouped_dict, current_matchday_int)
    """
    grouped = {}
    current_md = None
    for f in fixtures:
        md = f.get('matchday')
        if md not in grouped: grouped[md] = []
        grouped[md].append(f)
        
        if current_md is None and f.get('status') != 'FINISHED':
            current_md = md
            
    return grouped, current_md

def is_match_locked(kickoff_time_str):
    """Returns True if the match starts in less than 1 hour."""
    kickoff = datetime.fromisoformat(kickoff_time_str.replace('Z', '+00:00'))
    now = datetime.now(timezone.utc)
    return (kickoff - now) < timedelta(hours=1)

def get_score_display(match: dict) -> str:
    score_data = match.get("score", {}).get("fullTime", {})
    home_score = score_data.get("home")
    away_score = score_data.get("away")
    return f"{home_score} - {away_score}"


def get_user_predictions(supabase, user_id):
    """
    Accepts supabase as an argument.
    This makes the function "pure" and decoupled from environment variables.
    """
    response = supabase.table("predictions") \
        .select("fixture_id, prediction") \
        .eq("user_id", user_id) \
        .execute()

    return {item['fixture_id']: item['prediction'] for item in response.data}

def handle_prediction_save(supabase, user_id: str, fixture_id:str, user_choice:str ):
    prediction_data = {
        "user_id": user_id,
        "fixture_id": fixture_id,
        "prediction": user_choice  # Ensure this matches your column name in Supabase
    }
    supabase.table("predictions").upsert(prediction_data, on_conflict="user_id, fixture_id",).execute()

def get_upcoming_matches(all_fixtures:dict) -> list:
    """
    Filters out matches that have already finished.
    """
    # We want matches where status is NOT 'FINISHED'
    upcoming = [match for match in all_fixtures if match['status'] != 'FINISHED']
    return upcoming

def get_finished_matches(all_fixtures:dict) -> list:
    """
    Filters out matches that have already finished.
    """
    # We want matches where status is NOT 'FINISHED'
    finished_matches = [match for match in all_fixtures if match['status'] == 'FINISHED']
    return finished_matches