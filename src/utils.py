PL_CREST = "https://eu-images.contentstack.com/v3/assets/blt740a130ae3c5d529/blt3402b01ca1f6ac5a/650f094ae864c5cf53bb38c5/Premier_League.png?width=1280&auto=webp&quality=80&format=jpg&disable=upscale"

def get_team_name(match: dict, team: str):
    if team == "HOME":
        return match.get("homeTeam", {}).get("shortName", "Home TBD")
    else:
        # This was 'homeTeam' in your version; changed to 'awayTeam'
        return match.get("awayTeam", {}).get("shortName", "Away TBD")

def get_team_badge(match: dict, team: str):
    if team == "HOME":
        return match.get("homeTeam", {}).get("crest", "Home TBD")
    else:
        return match.get("awayTeam", {}).get("crest", "Away TBD")

