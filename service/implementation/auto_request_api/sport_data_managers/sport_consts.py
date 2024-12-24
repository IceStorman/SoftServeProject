from typing import Optional


def get_team_statistics_url(sport_name: str, team_id: Optional[int], league_id: Optional[int]):
    print("Getting team statistics url")
    match sport_name:
        case "afl":
            return f"https://v1.afl.api-sports.io/teams/statistics?id={team_id}&season=2023"
        case "rugby":
            return f"https://v1.rugby.api-sports.io/teams/statistics?season=2024&team={team_id}&league={league_id}"
        case "baseball":
            return f"https://v1.baseball.api-sports.io/teams/statistics?league={league_id}&season=2024&team={team_id}"
        case "handball":
            return f"https://v1.handball.api-sports.io/teams/statistics?season=2024&team={team_id}&league={league_id}"
        case "hockey":
            return f"https://v1.hockey.api-sports.io/teams/statistics?season=2024&team={team_id}&league={league_id}"
        case "volleyball":
            return f"https://v1.volleyball.api-sports.io/teams/statistics?season=2024&team={team_id}&league={league_id}"

def get_team_statistics_index(sport_name: str, team_id: Optional[int], league_id: Optional[int]):
    print("Getting team statistics index")
    match sport_name:
        case "afl":
            return f"teams/statistics?id={team_id}&season=2023"
        case "rugby":
            return f"teams/statistics?season=2024&team={team_id}&league={league_id}"
        case "handball":
            return f"teams/statistics?season=2024&team={team_id}&league={league_id}"
        case "hockey":
            return f"teams/statistics?season=2024&team={team_id}&league={league_id}"
        case "volleyball":
            return f"teams/statistics?season=2024&team={team_id}&league={league_id}"
        case "baseball":
            return f"teams/statistics?league={league_id}&season=2024&team={team_id}"


def get_host(sport_name: str):
    print("Getting host")
    match sport_name:
        case "afl":
            return "v1.afl.api-sports.io"
        case "rugby":
            return "v1.rugby.api-sports.io"
        case "baseball":
            return "v1.baseball.api-sports.io"
        case "handball":
            return "v1.handball.api-sports.io"
        case "hockey":
            return "v1.hockey.api-sports.io"
        case "volleyball":
            return "v1.volleyball.api-sports.io"
        case "nba":
            return "v2.nba.api-sports.io"
        case "basketball":
            return "v1.basketball.api-sports.io"
        case "football":
            return "v3.football.api-sports.io"
        case "formulaOne":
            return "v1.formula-1.api-sports.io"
        case "mma":
            return "v1.mma.api-sports.io"
        case "nfl":
            return "v1.american-football.api-sports.io"
