import os
from dotenv import load_dotenv
import requests
from datetime import datetime
from typing import Dict
from sqlalchemy import text
from database.session import SessionLocal
from database.azure_blob_storage.save_get_blob import blob_autosave_api

from database.postgres import save_api_data

load_dotenv()
api_key = [
    os.getenv("APIKEY1"),
    os.getenv("APIKEY2"),
    os.getenv("APIKEY3"),
    os.getenv("APIKEY4"),
    os.getenv("APIKEY5"),
    os.getenv("APIKEY6"),
    os.getenv("APIKEY7"),
    os.getenv("APIKEY8"),
    os.getenv("APIKEY9"),
    os.getenv("APIKEY10"),
]

apis = [
    {
        "name": "football",
        "index": "fixtures",
        "url": "https://v3.football.api-sports.io/fixtures?date=DATE",
        "host": "v3.football.api-sports.io",
        "frequency": 3
    },
    {
        "name": "football",
        "index": "timezone",
        "url": "https://v3.football.api-sports.io/timezone",
        "host": "v3.football.api-sports.io",
        "frequency": 1333
    },
    {
        "name": "football",
        "index": "countries",
        "url": "https://v3.football.api-sports.io/countries",
        "host":"v3.football.api-sports.io",
        "frequency": 1331
    },
    {
        "name": "football",
        "index": "leagues",
        "url": "https://v3.football.api-sports.io/leagues",
        "host":"v3.football.api-sports.io",
        "frequency": 1335
    },
    {
        "name": "baseball",
        "index": "leagues",
        "url": "https://v1.baseball.api-sports.io/leagues",
        "host": "v1.baseball.api-sports.io",
        "frequency": 1333
    },
    {
        "name": "baseball",
        "index": "games",
        "url": "https://v1.baseball.api-sports.io/games?date=DATE",
        "host": "v1.baseball.api-sports.io",
        "frequency": 3
    },
    {
        "name": "basketball",
        "index": "leagues",
        "url": "https://v1.basketball.api-sports.io/leagues",
        "host": "v1.basketball.api-sports.io",
        "frequency": 1334
    },
    {
        "name": "basketball",
        "index": "games",
        "url": "https://v1.basketball.api-sports.io/games?date=DATE",
        "host": "v1.basketball.api-sports.io",
        "frequency": 1.6
    },
    {
        "name": "formula-1",
        "index": "competitions",
        "url": "https://v1.formula-1.api-sports.io/competitions",
        "host": "v1.formula-1.api-sports.io",
        "frequency": 1299
    },
    {
        "name": "formula-1",
        "index": "circuits",
        "url": "https://v1.formula-1.api-sports.io/circuits",
        "host": "v1.formula-1.api-sports.io",
        "frequency": 1298
    },
    {
        "name": "formula-1",
        "index": "drivers?search=lewi",
        "url": "https://v1.formula-1.api-sports.io/drivers?search=lewi",
        "host": "v1.formula-1.api-sports.io",
        "frequency": 302
    },
    {
        "name": "formula-1",
        "index": "teams",
        "url": "https://v1.formula-1.api-sports.io/teams",
        "host": "v1.formula-1.api-sports.io",
        "frequency": 19999
    },
    {
        "name": "formula-1",
        "index": "races",
        "url": "https://v1.formula-1.api-sports.io/races?date=DATE",
        "host": "v1.formula-1.api-sports.io",
        "frequency": 11
    },
    {
        "name": "handball",
        "index": "countries",
        "url": "https://v1.handball.api-sports.io/countries",
        "host": "v1.handball.api-sports.io",
         "frequency": 1301
    },
    {
        "name": "handball",
        "index": "leagues",
        "url": "https://v1.handball.api-sports.io/leagues",
        "host": "v1.handball.api-sports.io",
        "frequency": 679
    },
    {
        "name": "handball",
        "index": "games",
        "url": "https://v1.handball.api-sports.io/games?date=DATE",
        "host": "v1.handball.api-sports.io",
        "frequency": 3
    },
    {
        "name": "hockey",
        "index": "countries",
        "url": "https://v1.hockey.api-sports.io/countries",
        "host": "v1.hockey.api-sports.io",
        "frequency": 1305
    },
    {
        "name": "hockey",
        "index": "leagues",
        "url": "https://v1.hockey.api-sports.io/leagues",
        "host": "v1.hockey.api-sports.io",
        "frequency": 670
    },
    {
        "name": "hockey",
        "index": "games",
        "url": "https://v1.hockey.api-sports.io/games?date=DATE",
        "host": "v1.hockey.api-sports.io",
        "frequency": 3
    },
    {
        "name": "mma",
        "index": "categories",
        "url": "https://v1.mma.api-sports.io/categories",
        "host": "v1.mma.api-sports.io",
        "frequency": 376
    },
    {
        "name": "mma",
        "index": "teams",
        "url": "https://v1.mma.api-sports.io/teams",
        "host": "v1.mma.api-sports.io",
        "frequency": 19999
    },
    {
        "name": "mma",
        "index": "fighters",
        "url": "https://v1.mma.api-sports.io/fighters?category=Flyweight",
        "host": "v1.mma.api-sports.io",
        "frequency": 311
    },
    {
        "name": "mma",
        "index": "fights",
        "url": "https://v1.mma.api-sports.io/fights?date=DATE",
        "host": "v1.mma.api-sports.io",
        "frequency": 5
    },
    {
        "name": "mma",
        "index": "fights-results",
        "url": "https://v1.mma.api-sports.io/fights/results?date=DATE",
        "host": "v1.mma.api-sports.io",
        "frequency": 7
    },
    {
        "name": "mma",
        "index": "fights-statistics-fighters",
        "url": "https://v1.mma.api-sports.io/fights/statistics/fighters?date=DATE",
        "host": "v1.mma.api-sports.io",
        "frequency": 16
    },
    {
        "name": "nfl",
        "index": "leagues",
        "url": "https://v1.american-football.api-sports.io/leagues",
        "host": "v1.american-football.api-sports.io",
        "frequency": 679
    },
    {
        "name": "nfl",
        "index": "games",
        "url": "https://v1.american-football.api-sports.io/games?date=DATE",
        "host": "v1.american-football.api-sports.io",
        "frequency": 4
    },
    {
        "name": "rugby",
        "index": "countries",
        "url": "https://v1.rugby.api-sports.io/countries",
        "host": "v1.rugby.api-sports.io",
        "frequency": 1303
    },
    {
        "name": "rugby",
        "index": "leagues",
        "url": "https://v1.rugby.api-sports.io/leagues",
        "host": "v1.rugby.api-sports.io",
        "frequency": 1308
    },
    {
        "name": "rugby",
        "index": "teams",
        "url": "https://v1.rugby.api-sports.io/teams?country=Argentina&league=1&season=2022",
        "host": "v1.rugby.api-sports.io",
        "frequency": 683
    },
    {
        "name": "rugby",
        "index": "games",
        "url": "https://v1.rugby.api-sports.io/games?date=DATE",
        "host": "v1.rugby.api-sports.io",
        "frequency": 4
    },
    {
        "name": "volleyball",
        "index": "countries",
        "url": "https://v1.volleyball.api-sports.io/countries",
        "host": "v1.volleyball.api-sports.io",
        "frequency": 1301
    },
    {
        "name": "volleyball",
        "index": "leagues",
        "url": "https://v1.volleyball.api-sports.io/leagues",
        "host": "v1.volleyball.api-sports.io",
        "frequency": 1298
    },
    {
        "name": "volleyball",
        "index": "games",
        "url": "https://v1.volleyball.api-sports.io/games?date=DATE",
        "host": "v1.volleyball.api-sports.io",
        "frequency": 3
    },
]
token_usage = {
    "football": { "current_key_index": 0 , "count": 0 },
    "basketball": { "current_key_index": 0 , "count": 0 },
    "volleyball": { "current_key_index": 0 , "count": 0 },
    "afl": { "current_key_index": 0 , "count": 0 },
    "baseball": { "current_key_index": 0 , "count": 0 },
    "formula-1": { "current_key_index": 0 , "count": 0 },
    "handball": { "current_key_index": 0 , "count": 0 },
    "hockey": { "current_key_index": 0 , "count": 0 },
    "mma": { "current_key_index": 0 , "count": 0 },
    "nba": { "current_key_index": 0 , "count": 0 },
    "nfl": { "current_key_index": 0 , "count": 0 },
    "rugby": { "current_key_index": 0 , "count": 0 },
}

def auto_request_system(api: Dict[str, str]) -> None:
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        url_with_date = api["url"].replace("DATE", today)
        if token_usage[api['name']]["count"] >= 99:
            token_usage[api['name']]["current_key_index"] = (token_usage[api['name']]["current_key_index"] + 1) % len(api_key)
            token_usage[api['name']]["count"] = 0
        token_usage[api['name']]["count"] += 1
        headers = {
            'x-rapidapi-host': api["host"],
            'x-rapidapi-key': api_key[token_usage[api['name']]["current_key_index"]]
        }
        response = requests.get(url_with_date, headers=headers, timeout=10)
        response.raise_for_status()
        json_data = response.json()
        #blob_autosave_api(json_data, api)

        save_api_data(json_data, api['name'])
    except requests.exceptions.RequestException as e:
        print(f"Error while making a request to {api['name']}: {e}")
    except Exception as e:
        print(f"General error while saving data for {api['name']}: {e}")


def keep_db_alive():
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
            print("Database connection is alive.")
    except Exception as e:
        print(f"Error keeping database connection alive: {e}")
