def get_team_statistics_url(sport_name: str, team_id: int, league_id: int):
    match sport_name:
        case "Afl":
            return f"https://v1.afl.api-sports.io/teams/statistics?id={team_id}&season=2023"
        case "Rugby":
            return f"https://v1.rugby.api-sports.io/teams/statistics?season=2024&team={team_id}&league={league_id}"
        case "Baseball":
            return f"https://v1.baseball.api-sports.io/teams/statistics?league={league_id}&season=2024&team={team_id}"
        case "Handball":
            return f"https://v1.handball.api-sports.io/teams/statistics?season=2024&team={team_id}&league={league_id}"
        case "Hockey":
            return f"https://v1.hockey.api-sports.io/teams/statistics?season=2024&team={team_id}&league={league_id}"
        case "Volleyball":
            return f"https://v1.volleyball.api-sports.io/teams/statistics?season=2024&team={team_id}&league={league_id}"

def get_team_statistics_index(sport_name: str, team_id: int, league_id: int):
    match sport_name:
        case "Afl":
            return f"teams/statistics?id={team_id}&season=2023"
        case "Rugby":
            return f"teams/statistics?season=2024&team={team_id}&league={league_id}"
        case "Handball":
            return f"teams/statistics?season=2024&team={team_id}&league={league_id}"
        case "Hockey":
            return f"teams/statistics?season=2024&team={team_id}&league={league_id}"
        case "Volleyball":
            return f"teams/statistics?season=2024&team={team_id}&league={league_id}"
        case "Baseball":
            return f"teams/statistics?league={league_id}&season=2024&team={team_id}"