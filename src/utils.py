def get_team_name(match: dict, team: str):
    if team == "HOME":
        return match.get("homeTeam", {}).get("shortName", "Home TBD")
    else:
        # This was 'homeTeam' in your version; changed to 'awayTeam'
        return match.get("awayTeam", {}).get("shortName", "Away TBD")