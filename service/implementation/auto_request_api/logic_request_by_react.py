import requests
from datetime import datetime
from logic_auto_request import current_key_index, token_usage, api_key
from database.azure_blob_storage.save_get_blob import blob_save_specific_api, get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict

def main_request(host, name, url, blob_name):
    global current_key_index, account_url
    today = datetime.now().strftime('%Y-%m-%d')
    if token_usage[name] >= 99:
        current_key_index = (current_key_index + 1) % len(api_key)
        token_usage[name] = 0
    token_usage[name] += 1
    headers = {
        'x-rapidapi-host': host,
        'x-rapidapi-key': api_key[current_key_index]
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    json_data = response.json()
    blob_save_specific_api(name, blob_name, json_data)
    return json_data

def football_fixtures_statistics(api_data: Dict[str, str]) -> Dict[str, str]:
    fixture_id = api_data.get("fixture_id")
    team_id = api_data.get("team_id")
    if not fixture_id or not team_id:
        return {"error": "Missing or invalid parameters: 'fixture_id' and 'team_id' are required."}
    name = "football"
    index = f"fixtures/statistics?fixture={fixture_id}&team={team_id}"
    with SessionLocal() as session:
        check = get_all_blob_indexes_from_db(session, index)
        if check:
            result = get_blob_data_for_all_sports(session, check)
            print("xui")
            return result
    print("xuiiiiiii")
    url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}&team={team_id}"
    host = "v3.football.api-sports.io"
    try:
        json_data = main_request(host, name, url, index)
        return json_data
    except Exception as e:
        return {"error": str(e)}

def football_fixtures_events_lineups_players(api_data: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    fixture_id = api_data.get("fixture_id")
    if not fixture_id :
        return {"error": {"message": "Missing or invalid parameter: 'fixture_id' required."}}
    name = "football"
    index1 = f"fixtures/events?fixture={fixture_id}"
    index2 = f"fixtures/lineups?fixture={fixture_id}"
    index3 = f"fixtures/players?fixture=1300109{fixture_id}"
    with SessionLocal() as session:
        check1 = get_all_blob_indexes_from_db(session, index1)
        check2 = get_all_blob_indexes_from_db(session, index2)
        check3 = get_all_blob_indexes_from_db(session, index3)
        if check1 and check2 and check3:
            result1 = get_blob_data_for_all_sports(session, check1)
            result2 = get_blob_data_for_all_sports(session, check2)
            result3 = get_blob_data_for_all_sports(session, check3)
            print("xui")
            return {
                "events": result1,
                "lineups": result2,
                "players": result3
            }
    print("xuiiiiiii")
    url1 = f"https://v3.football.api-sports.io/fixtures/events?fixture={fixture_id}"
    url2 = f"https://v3.football.api-sports.io/fixtures/lineups?fixture={fixture_id}"
    url3 = f"https://v3.football.api-sports.io/fixtures/players?fixture={fixture_id}"
    host = "v3.football.api-sports.io"
    try:
        json_data1 = main_request(host, name, url1, index1)
        json_data2 = main_request(host, name, url2, index2)
        json_data3 = main_request(host, name, url3, index3)
        return {
            "events": json_data1,
            "lineups": json_data2,
            "players": json_data3
        }
    except Exception as e:
        return {"error": {"message": str(e)}}

def football_coachs(api_data: Dict[str, str]) -> Dict[str, str]:
    team_id = api_data.get("team_id")
    if not team_id:
        return {"error": "Missing or invalid parameter: 'team_id' required."}
    name = "football"
    index = f"coachs/coachs?team={team_id}"
    with SessionLocal() as session:
        check = get_all_blob_indexes_from_db(session, index)
        if check:
            result = get_blob_data_for_all_sports(session, check)
            print("xui")
            return result
    url = f"https://v3.football.api-sports.io/coachs?team={team_id}"
    host = "v3.football.api-sports.io"
    try:
        json_data = main_request(host, name, url, index)
        return json_data
    except Exception as e:
        return {"error": str(e)}

def football_players_profiles_sidelined(api_data: Dict[str, str]) -> Dict[str, str]:
    player_id = api_data.get("player_id")
    if not player_id:
        return {"error": "Missing or invalid parameter: 'player_id' required."}
    name = "football"
    index1 = f"players/profiles?player={player_id}"
    index2 = f"players/players?id={player_id}&season=2024"
    index3 = f"players/sidelined?player={player_id}"
    with SessionLocal() as session:
        check1 = get_all_blob_indexes_from_db(session, index1)
        check2 = get_all_blob_indexes_from_db(session, index2)
        check3 = get_all_blob_indexes_from_db(session, index3)
        if check1 and check2 and check3:
            result1 = get_blob_data_for_all_sports(session, check1)
            result2 = get_blob_data_for_all_sports(session, check2)
            result3 = get_blob_data_for_all_sports(session, check3)
            print("xui")
            return {
                "profiles": result1,
                "players": result2,
                "sidelined": result3
            }
    url1 = f"https://v3.football.api-sports.io/players/profiles?player=276{player_id}"
    url2 = f"https://v3.football.api-sports.io/players?id={player_id}&season=2024"
    url3 = f"https://v3.football.api-sports.io/sidelined?player={player_id}"
    host = "v3.football.api-sports.io"
    try:
        json_data1 = main_request(host, name, url1, index1)
        json_data2 = main_request(host, name, url2, index2)
        json_data3 = main_request(host, name, url3, index3)
        return {
            "profiles": json_data1,
            "players": json_data2,
            "sidelined": json_data3
        }
    except Exception as e:
        return {"error": str(e)}

def afl_teams_statistics(api_data: Dict[str, str]) -> Dict[str, str]:
    team_id = api_data.get("team_id")
    if not team_id:
        return {"error": "Missing or invalid parameter: 'team_id' required."}
    name = "afl"
    index = f"teams/statistics?id={team_id}&season=2023"
    with SessionLocal() as session:
        check = get_all_blob_indexes_from_db(session, index)
        if check:
            result = get_blob_data_for_all_sports(session, check)
            print("xui")
            return result
    url = f"https://v1.afl.api-sports.io/teams/statistics?id={team_id}&season=2023"
    host = "v1.afl.api-sports.io"
    try:
        json_data = main_request(host, name, url, index)
        return json_data
    except Exception as e:
        return {"error": str(e)}

def afl_players(api_data: Dict[str, str]) -> Dict[str, str]:
    team_id = api_data.get("team_id")
    if not team_id:
        return {"error": "Missing or invalid parameter: 'team_id' required."}
    name = "afl"
    index = f"teams/players?season=2023&team={team_id}"
    with SessionLocal() as session:
        check = get_all_blob_indexes_from_db(session, index)
        if check:
            result = get_blob_data_for_all_sports(session, check)
            print("xui")
            return result
    url = f"https://v1.afl.api-sports.io/players?season=2023&team={team_id}"
    host = "v1.afl.api-sports.io"
    try:
        json_data = main_request(host, name, url, index)
        return json_data
    except Exception as e:
        return {"error": str(e)}

def afl_players_statistics(api_data: Dict[str, str]) -> Dict[str, str]:
    player_id = api_data.get("player_id")
    if not player_id:
        return {"error": "Missing or invalid parameter: 'player_id' required."}
    name = "afl"
    index = f"players/statistics?id={player_id}&season=2024"
    with SessionLocal() as session:
        check = get_all_blob_indexes_from_db(session, index)
        if check:
            result = get_blob_data_for_all_sports(session, check)
            print("xui")
            return result
    url = f"https://v1.afl.api-sports.io/players/statistics?id={player_id}&season=2024"
    host = "v1.afl.api-sports.io"
    try:
        json_data = main_request(host, name, url, index)
        return json_data
    except Exception as e:
        return {"error": str(e)}

def baseball_teams_statistics(api_data: Dict[str, str]) -> Dict[str, str]:
    team_id = api_data.get("team_id")
    league_id = api_data.get("league_id")
    if not team_id or not league_id:
        return {"error": "Missing or invalid parameter: 'team_id' and 'league_id' are required."}
    name = "baseball"
    index = f"teams/statistics?league={league_id}&season=2024&team={team_id}"
    with SessionLocal() as session:
        check = get_all_blob_indexes_from_db(session, index)
        if check:
            result = get_blob_data_for_all_sports(session, check)
            print("xui")
            return result
    url = f"https://v1.baseball.api-sports.io/teams/statistics?league={league_id}&season=2024&team={team_id}"
    host = "v1.baseball.api-sports.io"
    try:
        json_data = main_request(host, name, url, index)
        return json_data
    except Exception as e:
        return {"error": str(e)}

def basketball_players(api_data: Dict[str, str]) -> Dict[str, str]:
    team_id = api_data.get("team_id")
    if not team_id:
        return {"error": "Missing or invalid parameter: 'team_id' required."}
    name = "basketball"
    index = f"players/players?team={team_id}&season=2024"
    with SessionLocal() as session:
        check = get_all_blob_indexes_from_db(session, index)
        if check:
            result = get_blob_data_for_all_sports(session, check)
            print("xui")
            return result
    url = f"https://v1.basketball.api-sports.io/players?team={team_id}&season=2024"
    host = "v1.basketball.api-sports.io"
    try:
        json_data = main_request(host, name, url, index)
        return json_data
    except Exception as e:
        return {"error": str(e)}

def basketball_players_statistics(api_data: Dict[str, str]) -> Dict[str, str]:
    player_id = api_data.get("player_id")
    if not player_id:
        return {"error": "Missing or invalid parameter: 'player_id' required."}
    name = "basketball"
    index = f"players/games/statistics/players?id={player_id}"
    with SessionLocal() as session:
        check = get_all_blob_indexes_from_db(session, index)
        if check:
            result = get_blob_data_for_all_sports(session, check)
            print("xui")
            return result
    url = f"https://v1.basketball.api-sports.io/games/statistics/players?id={player_id}"
    host = "v1.basketball.api-sports.io"
    try:
        json_data = main_request(host, name, url, index)
        return json_data
    except Exception as e:
        return {"error": str(e)}

def formula_one_rankings_races_and_fastestlaps(api_data: Dict[str, str]) -> Dict[str, str]:
    race_id = api_data.get("race_id")
    if not race_id:
        return {"error": "Missing or invalid parameter: 'race_id' required."}
    name = "formula-1"
    index1 = f"rankings/races?race={race_id}"
    index2 = f"rankings/fastestlaps?race={race_id}"
    with SessionLocal() as session:
        check1 = get_all_blob_indexes_from_db(session, index1)
        check2 = get_all_blob_indexes_from_db(session, index2)
        if check1 and check2:
            result1 = get_blob_data_for_all_sports(session, check1)
            result2 = get_blob_data_for_all_sports(session, check2)
            print("xui")
            return {
                "races": result1,
                "fastestlaps": result2,
            }
    url1 = f"https://v1.formula-1.api-sports.io/rankings/races?race={race_id}"
    url2 = f"https://v1.formula-1.api-sports.io/rankings/fastestlaps?race={race_id}"
    host = "v1.formula-1.api-sports.io"
    try:
        json_data1 = main_request(host, name, url1, index1)
        json_data2 = main_request(host, name, url2, index2)
        return {
            "races": json_data1,
            "fastestlaps": json_data2,
        }
    except Exception as e:
        return {"error": str(e)}

def handball_teams_statistics(api_data: Dict[str, str]) -> Dict[str, str]:
    team_id = api_data.get("team_id")
    league_id = api_data.get("league_id")
    if not team_id or not league_id:
        return {"error": "Missing or invalid parameter: 'team_id' and 'league_id' are required."}
    name = "handball"
    index = f"teams/statistics?season=2024&team={team_id}&league={league_id}"
    with SessionLocal() as session:
        check = get_all_blob_indexes_from_db(session, index)
        if check:
            result = get_blob_data_for_all_sports(session, check)
            print("xui")
            return result
    url = f"https://v1.handball.api-sports.io/teams/statistics?season=2024&team={team_id}&league={league_id}"
    host = "v1.handball.api-sports.io"
    try:
        json_data = main_request(host, name, url, index)
        return json_data
    except Exception as e:
        return {"error": str(e)}

def hockey_teams_statistics(api_data: Dict[str, str]) -> Dict[str, str]:
    team_id = api_data.get("team_id")
    league_id = api_data.get("league_id")
    if not team_id or not league_id:
        return {"error": "Missing or invalid parameter: 'team_id' and 'league_id' are required."}
    name = "hockey"
    index = f"teams/statistics?season=2024&team={team_id}&league={league_id}"
    with SessionLocal() as session:
        check = get_all_blob_indexes_from_db(session, index)
        if check:
            result = get_blob_data_for_all_sports(session, check)
            print("xui")
            return result
    url = f"https://v1.hockey.api-sports.io/teams/statistics?season=2024&team={team_id}&league={league_id}"
    host = "v1.hockey.api-sports.io"
    try:
        json_data = main_request(host, name, url, index)
        return json_data
    except Exception as e:
        return {"error": str(e)}

def hockey_games_events(api_data: Dict[str, str]) -> Dict[str, str]:
    game_id = api_data.get("game_id")
    if not game_id:
        return {"error": "Missing or invalid parameter: 'game_id' required."}
    name = "hockey"
    index = f"games/events?game={game_id}"
    with SessionLocal() as session:
        check = get_all_blob_indexes_from_db(session, index)
        if check:
            result = get_blob_data_for_all_sports(session, check)
            print("xui")
            return result
    url = f"https://v1.hockey.api-sports.io/games/events?game={game_id}"
    host = "v1.hockey.api-sports.io"
    try:
        json_data = main_request(host, name, url, index)
        return json_data
    except Exception as e:
        return {"error": str(e)}

def mma_fighters_records(api_data: Dict[str, str]) -> Dict[str, str]:
    player_id = api_data.get("player_id")
    if not player_id:
        return {"error": "Missing or invalid parameter: 'player_id' required."}
    name = "mma"
    index = f"fighters/records?id={player_id}"
    with SessionLocal() as session:
        check = get_all_blob_indexes_from_db(session, index)
        if check:
            result = get_blob_data_for_all_sports(session, check)
            print("xui")
            return result
    url = f"https://v1.mma.api-sports.io/fighters/records?id={player_id}"
    host = "v1.mma.api-sports.io"
    try:
        json_data = main_request(host, name, url, index)
        return json_data
    except Exception as e:
        return {"error": str(e)}

def nba_games_statistics(api_data: Dict[str, str]) -> Dict[str, str]:
    game_id = api_data.get("game_id")
    if not game_id:
        return {"error": "Missing or invalid parameter: 'game_id' required."}
    name = "nba"
    index = f"games/statistics?id={game_id}"
    with SessionLocal() as session:
        check = get_all_blob_indexes_from_db(session, index)
        if check:
            result = get_blob_data_for_all_sports(session, check)
            print("xui")
            return result
    url = f"https://v2.nba.api-sports.io/games/statistics?id={game_id}"
    host = "v2.nba.api-sports.io"
    try:
        json_data = main_request(host, name, url, index)
        return json_data
    except Exception as e:
        return {"error": str(e)}

def nfl_injuries_players(api_data: Dict[str, str]) -> Dict[str, str]:
    team_id = api_data.get("team_id")
    if not team_id:
        return {"error": "Missing or invalid parameter: 'team_id' required."}
    name = "nfl"
    index1 = f"injuries/injuries?team={team_id}"
    index2 = f"players/players?team={team_id}"
    with SessionLocal() as session:
        check1 = get_all_blob_indexes_from_db(session, index1)
        check2 = get_all_blob_indexes_from_db(session, index2)
        if check1 and check2:
            result1 = get_blob_data_for_all_sports(session, check1)
            result2 = get_blob_data_for_all_sports(session, check2)
            print("xui")
            return {
                "injuries": result1,
                "players": result2,
            }
    url1 = f"https://v1.american-football.api-sports.io/injuries?team={team_id}"
    url2 = f"https://v1.american-football.api-sports.io/players?team={team_id}"
    host = "v1.american-football.api-sports.io"
    try:
        json_data1 = main_request(host, name, url1, index1)
        json_data2 = main_request(host, name, url2, index2)
        return {
            "injuries": json_data1,
            "players": json_data2,
        }
    except Exception as e:
        return {"error": str(e)}

def rugby_teams_statistics(api_data: Dict[str, str]) -> Dict[str, str]:
    team_id = api_data.get("team_id")
    league_id = api_data.get("league_id")
    if not team_id or not league_id:
        return {"error": "Missing or invalid parameter: 'team_id' and 'league_id' are required."}
    name = "rugby"
    index = f"teams/statistics?season=2024&team={team_id}&league={league_id}"
    with SessionLocal() as session:
        check = get_all_blob_indexes_from_db(session, index)
        if check:
            result = get_blob_data_for_all_sports(session, check)
            print("xui")
            return result
    url = f"https://v1.rugby.api-sports.io/teams/statistics?season=2024&team={team_id}&league={league_id}"
    host = "v1.rugby.api-sports.io"
    try:
        json_data = main_request(host, name, url, index)
        return json_data
    except Exception as e:
        return {"error": str(e)}

def volleyball_teams_statistics(api_data: Dict[str, str]) -> Dict[str, str]:
    team_id = api_data.get("team_id")
    league_id = api_data.get("league_id")
    if not team_id or not league_id:
         return {"error": "Missing or invalid parameter: 'team_id' and 'league_id' are required."}
    name = "volleyball"
    index = f"teams/statistics?season=2024&team={team_id}&league={league_id}"
    with SessionLocal() as session:
        check = get_all_blob_indexes_from_db(session, index)
        if check:
            result = get_blob_data_for_all_sports(session, check)
            print("xui")
            return result
    url = f"https://v1.volleyball.api-sports.io/teams/statistics?season=2024&team={team_id}&league={league_id}"
    host = "v1.volleyball.api-sports.io"
    try:
        json_data = main_request(host, name, url, index)
        return json_data
    except Exception as e:
        return {"error": str(e)}


api1 = {"fixture_id": 380516, "team_id": 103}
result=football_fixtures_statistics(api1)
print(result)
api2 = {"fixture_id": 123456}
result=football_fixtures_events_lineups_players(api2)
print(result)
api3 = {"team_id": 234}
result=football_coachs(api3)
print(result)
api4 = {"player_id": 234}
result=football_players_profiles_sidelined(api4)
print(result)
api5 = {"team_id": 123}
result=afl_teams_statistics(api5)
print(result)
api6 = {"team_id": 123}
result=afl_players(api6)
print(result)
api7 = {"player_id": 234}
result=afl_players_statistics(api7)
print(result)
api8 = {"league_id": 3, "team_id": 123}
result=baseball_teams_statistics(api8)
print(result)
api9 = {"team_id": 333}
result=basketball_players(api9)
print(result)
api10 = {"player_id": 234}
result=basketball_players_statistics(api10)
print(result)
api11 = {"race_id": 2}
result=formula_one_rankings_races_and_fastestlaps(api11)
print(result)
api12 = {"league_id": 3, "team_id": 123}
result=handball_teams_statistics(api12)
print(result)
api13 = {"league_id": 3, "team_id": 123}
result=hockey_teams_statistics(api13)
print(result)
api14 = {"game_id": 1234}
result=hockey_games_events(api14)
print(result)
api15 = {"player_id": 123}
result=mma_fighters_records(api15)
print(result)
api16 = {"game_id": 1234}
result=nba_games_statistics(api16)
print(result)
api17 = {"team_id": 123}
result=nfl_injuries_players(api17)
print(result)
api18 = {"league_id": 3, "team_id": 123}
result=rugby_teams_statistics(api18)
print(result)
api19 = {"league_id": 3, "team_id": 123}
result=volleyball_teams_statistics(api19)
print(result)
'''

'''



