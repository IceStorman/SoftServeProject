import requests
import json
from azure.storage.blob import BlobServiceClient
from datetime import datetime
from logic_auto_request import current_key_index, token_usage, api_key, sports_dict, account_url
from typing import Dict

'''
    {
        "name": "football",
        "index": "fixtures",
        "url": "https://v3.football.api-sports.io/fixtures?date=DATE",
        "host": "v3.football.api-sports.io",
        "frequency": 1 #5  # Інтервал у хвилинах
    },
'''

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
    selected_sport = name
    key = sports_dict[selected_sport]
    blob_service_client = BlobServiceClient(account_url=account_url, credential=key)
    container_client = blob_service_client.get_container_client(name)
    blob_name = f"{blob_name}.json"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(json.dumps(json_data), overwrite=True)
    return json_data

def football_fixtures_statistics(api_data: Dict[str, str]) -> Dict[str, str]:
    fixture_id = api_data.get("fixture_id")
    team_id = api_data.get("team_id")
    if not fixture_id or not team_id:
        return {"error": "Missing or invalid parameters: 'fixture_id' and 'team_id' are required."}

    name = "football"
    index = f"fixtures/statistics?fixture={fixture_id}&team={team_id}"

    def db_check_logic():
        pass

    url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}&team={team_id}"
    host = "v3.football.api-sports.io"
    try:
        json_data = main_request(host, name, url, index)
        return json_data
    except Exception as e:
        # Повертаємо повідомлення про помилку
        return {"error": str(e)}

def football_fixtures_events_lineups_players(api_data: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    fixture_id = api_data.get("fixture_id")
    if not fixture_id :
        return {"error": {"message": "Missing or invalid parameter: 'fixture_id' required."}}

    name = "football"
    index1 = f"fixtures/events?fixture={fixture_id}"
    index2 = f"fixtures/lineups?fixture={fixture_id}"
    index3 = f"fixtures/players?fixture=1300109{fixture_id}"

    def db_check_logic():
        pass

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

    def db_check_logic():
        pass

    url = f"https://v3.football.api-sports.io/coachs?team={team_id}"
    host = "v3.football.api-sports.io"
    try:
        json_data = main_request(host, name, url, index)
        return json_data
    except Exception as e:
        # Повертаємо повідомлення про помилку
        return {"error": str(e)}

def football_players_profiles(api_data: Dict[str, str]) -> Dict[str, str]:
    player_id = api_data.get("player_id")
    if not player_id:
        return {"error": "Missing or invalid parameter: 'player_id' required."}
    name = "football"
    index = f"players/profiles?player={player_id}"

    def db_check_logic():
        pass

    url = f"https://v3.football.api-sports.io/players/profiles?player=276{player_id}"
    host = "v3.football.api-sports.io"
    try:
        json_data = main_request(host, name, url, index)
        return json_data
    except Exception as e:
        # Повертаємо повідомлення про помилку
        return {"error": str(e)}



api_data = {"fixture_id": 1300109, "team_id": 231}
api_data2 = {"team_id": 228}
api_data3 = {"fixture_id": 1300109, "player_id": 1234}
api_data4 = {"fixture_id": 1300109}

result = football_fixtures_statistics(api_data3)
result1 = football_fixtures_events_lineups_players(api_data3)
result2 = football_coachs(api_data2)
result3 = football_players_profiles(api_data3)

print(result)
print(result1)
print(result2)
print(result3)


