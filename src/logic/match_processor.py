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