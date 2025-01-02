from typing import Optional


def get_team_statistics_url(sport_id: int, team_id: Optional[int], league_id: Optional[int]):
    print("Getting team statistics url")
    match sport_id:
        case 3:
            return f"https://v1.handball.api-sports.io/teams/statistics?season=2024&team={team_id}&league={league_id}"
        case 4:
            return f"https://v1.hockey.api-sports.io/teams/statistics?season=2024&team={team_id}&league={league_id}"
        case 5:
            return f"https://v1.afl.api-sports.io/teams/statistics?id={team_id}&season=2023"
        case 6:
            return f"https://v1.rugby.api-sports.io/teams/statistics?season=2024&team={team_id}&league={league_id}"
        case 7:
            return f"https://v1.baseball.api-sports.io/teams/statistics?league={league_id}&season=2024&team={team_id}"
        case 9:
            return f"https://v1.volleyball.api-sports.io/teams/statistics?season=2024&team={team_id}&league={league_id}"

def get_team_statistics_index(sport_id: int, team_id: Optional[int], league_id: Optional[int]):
    print("Getting team statistics index")
    match sport_id:
        case 3:
            return f"teams/statistics?season=2024&team={team_id}&league={league_id}"
        case 4:
            return f"teams/statistics?season=2024&team={team_id}&league={league_id}"
        case 5:
            return f"teams/statistics?id={team_id}&season=2023"
        case 6:
            return f"teams/statistics?season=2024&team={team_id}&league={league_id}"
        case 7:
            return f"teams/statistics?season=2024&team={team_id}&league={league_id}"
        case 9:
            return f"teams/statistics?league={league_id}&season=2024&team={team_id}"


def get_host(sport_id: int):
    print("Getting host")
    match sport_id:
        case 1:
            return "v1.formula-1.api-sports.io"
        case 2:
            return "v2.nba.api-sports.io"
        case 3:
            return "v1.hockey.api-sports.io"
        case 4:
            return "v1.volleyball.api-sports.io"
        case 5:
            return "v1.afl.api-sports.io"
        case 6:
            return "v1.rugby.api-sports.io"
        case 7:
            return "v1.handball.api-sports.io"
        case 8:
            return "v3.football.api-sports.io"
        case 9:
            return "v1.baseball.api-sports.io"
        case 10:
            return "v1.basketball.api-sports.io"
        case 11:
            return "v1.mma.api-sports.io"
        case 12:
            return "v1.american-football.api-sports.io"

def get_sport_name(sport_id: int):
    match sport_id:
        case 1:
            return "formula-1"
        case 2:
            return "nba"
        case 3:
            return "hockey"
        case 4:
            return "volleyball"
        case 5:
            return "afl"
        case 6:
            return "rugby"
        case 7:
            return "handball"
        case 8:
            return "football"
        case 9:
            return "baseball"
        case 10:
            return "basketball"
        case 11:
            return "mma"
        case 12:
            return "nfl"