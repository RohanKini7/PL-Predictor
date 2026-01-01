PL_CREST = "https://s.yimg.com/ny/api/res/1.2/LphMBtd9JdHMl9V4Gmo2Iw--/YXBwaWQ9aGlnaGxhbmRlcjt3PTIwMDA7aD0xMTI2O2NmPXdlYnA-/https://media.zenfs.com/en/creative_bloq_161/87fefa9e5a05f4e3b07c88f2fe805fcc"

def get_team_name(match: dict, team: str):
    if team == "HOME":
        return match.get("homeTeam", {}).get("tla", "Home TBD")
    else:
        # This was 'homeTeam' in your version; changed to 'awayTeam'
        return match.get("awayTeam", {}).get("tla", "Away TBD")

def get_team_badge(match: dict, team: str):
    if team == "HOME":
        return match.get("homeTeam", {}).get("crest", "Home TBD")
    else:
        return match.get("awayTeam", {}).get("crest", "Away TBD")

