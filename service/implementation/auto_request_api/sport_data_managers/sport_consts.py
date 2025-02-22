from typing import Optional
from enum import Enum

class SportType(Enum):
    handball = "handball"
    hockey = "hockey"
    afl = "afl"
    rugby = "rugby"
    baseball = "baseball"
    basketball = "basketball"
    volleyball = "volleyball"
    football = "football"
    nfl = "nfl"
    mma = "mma"
    formula_1 = "formula-1"

def get_sport_type(sport_id: str) -> Optional[SportType]:
    try:
        sport_name = sport_id.replace('_', '-').lower()
        sport_type = SportType(sport_name)
        return sport_type
    except ValueError:
        print(f"Invalid sport_id: {sport_id}")
        return None

def get_team_statistics_url(sport_id: str, team_id: Optional[int], league_id: Optional[int]):
    sport_type = get_sport_type(sport_id)

    match sport_type:
        case SportType.handball:
            return f"https://v1.handball.api-sports.io/teams/statistics?season=2022&team={team_id}&league={league_id}"
        case SportType.hockey:
            return f"https://v1.hockey.api-sports.io/teams/statistics?season=2022&team={team_id}&league={league_id}"
        case SportType.afl:
            return f"https://v1.afl.api-sports.io/teams/statistics?id={team_id}&season=2022"
        case SportType.rugby:
            return f"https://v1.rugby.api-sports.io/teams/statistics?season=2022&team={team_id}&league={league_id}"
        case SportType.baseball:
            return f"https://v1.baseball.api-sports.io/teams/statistics?league={league_id}&season=2022&team={team_id}"
        case SportType.volleyball:
            return f"https://v1.volleyball.api-sports.io/teams/statistics?season=2022&team={team_id}&league={league_id}"

def get_team_statistics_index(sport_id: str, team_id: Optional[int], league_id: Optional[int]):
    sport_type = get_sport_type(sport_id)

    match sport_type:
        case SportType.handball:
            return f"teams/statistics?season=2022&team={team_id}&league={league_id}"
        case SportType.hockey:
            return f"teams/statistics?season=2022&team={team_id}&league={league_id}"
        case SportType.afl:
            return f"teams/statistics?id={team_id}&season=2022"
        case SportType.rugby:
            return f"teams/statistics?season=2022&team={team_id}&league={league_id}"
        case SportType.baseball:
            return f"teams/statistics?season=2022&team={team_id}&league={league_id}"
        case SportType.volleyball:
            return f"teams/statistics?league={league_id}&season=2022&team={team_id}"

def get_team_index(sport_id: str, league_id: Optional[int]):
    print("Getting team index")

    match get_sport_type(sport_id):
        case SportType.formula_1:
            return f"teams/teams"
        case SportType.mma:
            return f"teams/teams"
        case _:
            return f"teams/teams?season=2022&league={league_id}"

def get_players_url(sport_id: str, team_id: Optional[int], league_id: Optional[int], search: Optional[str]):
    sport_type = get_sport_type(sport_id)

    match sport_type:
        case SportType.nfl:
            return f"https://v1.american-football.api-sports.io/players?{f"&team={team_id}&season=2022" if team_id else ""}{f"&search={search}" if search else ""}"
        case SportType.mma:
            return f"https://v1.mma.api-sports.io/fighters?{f"&team={team_id}" if team_id else ""}{f"&search={search}" if search else ""}"
        case SportType.football:
            return f"https://v3.football.api-sports.io/players?season=2022{f"&team={team_id}" if team_id else ""}{f"&league={league_id}" if league_id else ""}{f"&search={search}" if search else ""}"
        case SportType.basketball:
            return f"https://v1.basketball.api-sports.io/players?{f"&team={team_id}&season=2022-2023" if team_id else ""}{f"&search={search}" if search else ""}"

def get_players_index(sport_id: str, team_id: Optional[int], league_id: Optional[int], search: Optional[str]):
    sport_type = get_sport_type(sport_id)

    match sport_type:
        case SportType.nfl:
            return f"teams/players?{f"&team={team_id}&season=2022" if team_id else ""}{f"&search={search}" if search else ""}"
        case SportType.mma:
            return f"teams/players?{f"&team={team_id}" if team_id else ""}{f"&search={search}" if search else ""}"
        case SportType.football:
            return f"teams/players?season=2022{f"&team={team_id}" if team_id else ""}{f"&league={league_id}" if league_id else ""}{f"&search={search}" if search else ""}"
        case SportType.basketball:
            return f"teams/players?{f"&team={team_id}&season=2022-2023" if team_id else ""}{f"&search={search}" if search else ""}"

def get_host(sport_id: str) -> Optional[str]:
    print("Getting host")

    sport_type = get_sport_type(sport_id)
    match sport_type:
        case SportType.formula_1:
            return "v1.formula-1.api-sports.io"
        case SportType.hockey:
            return "v1.hockey.api-sports.io"
        case SportType.volleyball:
            return "v1.volleyball.api-sports.io"
        case SportType.afl:
            return "v1.afl.api-sports.io"
        case SportType.rugby:
            return "v1.rugby.api-sports.io"
        case SportType.handball:
            return "v1.handball.api-sports.io"
        case SportType.football:
            return "v3.football.api-sports.io"
        case SportType.baseball:
            return "v1.baseball.api-sports.io"
        case SportType.basketball:
            return "v1.basketball.api-sports.io"
        case SportType.mma:
            return "v1.mma.api-sports.io"
        case SportType.nfl:
            return "v1.american-football.api-sports.io"