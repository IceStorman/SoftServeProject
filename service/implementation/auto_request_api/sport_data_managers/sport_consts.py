from typing import Optional


def get_team_statistics_url(sport_name: str, team_id: Optional[int], league_id: Optional[int]):
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

def get_team_statistics_index(sport_name: str, team_id: Optional[int], league_id: Optional[int]):
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


def get_host(sport_name: str):
    match sport_name:
        case "Afl":
            return "v1.afl.api-sports.io"
        case "Rugby":
            return "v1.rugby.api-sports.io"
        case "Baseball":
            return "v1.baseball.api-sports.io"
        case "Handball":
            return "v1.handball.api-sports.io"
        case "Hockey":
            return "v1.hockey.api-sports.io"
        case "Volleyball":
            return "v1.volleyball.api-sports.io"
        case "Nba":
            return "v2.nba.api-sports.io"
        case "Basketball":
            return "v1.basketball.api-sports.io"
        case "Football":
            return "v3.football.api-sports.io"
        case "FormulaOne":
            return "v1.formula-1.api-sports.io"
        case "Mma":
            return "v1.mma.api-sports.io"
        case "Nfl":
            return "v1.american-football.api-sports.io"
