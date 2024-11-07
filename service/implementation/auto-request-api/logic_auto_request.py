from azure.storage.blob import BlobServiceClient
import json
import os
from dotenv import load_dotenv
import requests
from datetime import datetime
from typing import Dict

load_dotenv()
api_key = [os.getenv("APIKEY"), "API_KEY_2", "API_KEY_3"]
current_key_index = 0
account_url = os.getenv("BLOBURL")

apis = [
    {
        "name": "football",
        "index": "fixtures",
        "url": "https://v3.football.api-sports.io/fixtures?date=DATE",
        "host": "v3.football.api-sports.io",
        "frequency": 1 #5  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "timezone",
        "url": "https://v3.football.api-sports.io/timezone",
        "host": "v3.football.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "countries",
        "url": "https://v3.football.api-sports.io/countries",
        "host":"v3.football.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "leagues",
        "url": "https://v3.football.api-sports.io/leagues",
        "host":"v3.football.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "teams",
        "url": "https://v3.football.api-sports.io/teams?country=Ukraine",
        "host": "v3.football.api-sports.io",
         "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "venues",
        "url": "https://v3.football.api-sports.io/venues?country=Ukraine",
        "host": "v3.football.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "injuries",
        "url": "https://v3.football.api-sports.io/injuries?date=DATE",
        "host": "v3.football.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-leagues",
        "url": "https://v1.afl.api-sports.io/leagues",
        "host": "v1.afl.api-sports.io",
        "frequency": 1 #1199  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-teams",
        "url": "https://v1.afl.api-sports.io/teams",
        "host": "v1.afl.api-sports.io",
        "frequency": 1 #600  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-games",
        "url": "https://v1.afl.api-sports.io/games?date=DATE",
        "host": "v1.afl.api-sports.io",
        "frequency": 1 #13  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-games-quarters?",
        "url": "https://v1.afl.api-sports.io/games/quarters?date=DATE",
        "host": "v1.afl.api-sports.io",
        "frequency": 1 #20  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-games-events",
        "url": "https://v1.afl.api-sports.io/games/events?date=DATE",
        "host": "v1.afl.api-sports.io",
        "frequency": 1 #23  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-games-statistics-teams",
        "url": "https://v1.afl.api-sports.io/games/statistics/teams?date=DATE",
        "host": "v1.afl.api-sports.io",
        "frequency": 1 #21 # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-games-statistics-players",
        "url": "https://v1.afl.api-sports.io/games/statistics/players?date=DATE",
        "host": "v1.afl.api-sports.io",
        "frequency": 1 #22 # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "leagues",
        "url": "https://v1.baseball.api-sports.io/leagues",
        "host": "v1.baseball.api-sports.io",
        "frequency": 1 #1200 # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "teams",
        "url": "https://v1.baseball.api-sports.io/teams",
        "host": "v1.baseball.api-sports.io",
        "frequency": 1 #600 # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "games",
        "url": "https://v1.baseball.api-sports.io/games?date=DATE",
        "host": "v1.baseball.api-sports.io",
        "frequency": 1 #15 # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "leagues",
        "url": "https://v1.basketball.api-sports.io/leagues",
        "host": "v1.basketball.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "teams",
        "url": "https://v1.basketball.api-sports.io/teams",
        "host": "v1.basketball.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "games",
        "url": "https://v1.basketball.api-sports.io/games?date=DATE",
        "host": "v1.basketball.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "formula-1",
        "index": "competitions",
        "url": "https://v1.formula-1.api-sports.io/competitions",
        "host": "v1.formula-1.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "formula-1",
        "index": "circuits",
        "url": "https://v1.formula-1.api-sports.io/circuits",
        "host": "v1.formula-1.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "formula-1",
        "index": "teams",
        "url": "https://v1.formula-1.api-sports.io/teams",
        "host": "v1.formula-1.api-sports.io",
         "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "formula-1",
        "index": "drivers?search=lewi",
        "url": "https://v1.formula-1.api-sports.io/drivers?search=lewi",
        "host": "v1.formula-1.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "formula-1",
        "index": "races",
        "url": "https://v1.formula-1.api-sports.io/races?date=DATE",
        "host": "v1.formula-1.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "handball",
        "index": "countries",
        "url": "https://v1.handball.api-sports.io/countries",
        "host": "v1.handball.api-sports.io",
         "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "handball",
        "index": "leagues",
        "url": "https://v1.handball.api-sports.io/leagues",
        "host": "v1.handball.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "handball",
        "index": "teams",
        "url": "https://v1.handball.api-sports.io/teams?country=Ukraine",
        "host": "v1.handball.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "handball",
        "index": "games",
        "url": "https://v1.handball.api-sports.io/games?date=DATE",
        "host": "v1.handball.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "countries",
        "url": "https://v1.hockey.api-sports.io/countries",
        "host": "v1.hockey.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "leagues",
        "url": "https://v1.hockey.api-sports.io/leagues",
        "host": "v1.hockey.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "teams",
        "url": "https://v1.hockey.api-sports.io/teams?country=Ukraine",
        "host": "v1.hockey.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "games",
        "url": "https://v1.hockey.api-sports.io/games?date=DATE",
        "host": "v1.hockey.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "categories",
        "url": "https://v1.mma.api-sports.io/categories",
        "host": "v1.mma.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "teams",
        "url": "https://v1.mma.api-sports.io/teams",
        "host": "v1.mma.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "fighters",
        "url": "https://v1.mma.api-sports.io/fighters?category=Flyweight",
        "host": "v1.mma.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "fights",
        "url": "https://v1.mma.api-sports.io/fights?date=DATE",
        "host": "v1.mma.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "fights-results",
        "url": "https://v1.mma.api-sports.io/fights/results?date=DATE",
        "host": "v1.mma.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "fights-statistics-fighters",
        "url": "https://v1.mma.api-sports.io/fights/statistics/fighters?date=DATE",
        "host": "v1.mma.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nba",
        "index": "leagues",
        "url": "https://v2.nba.api-sports.io/leagues",
        "host": "v2.nba.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nba",
        "index": "games",
        "url": "https://v2.nba.api-sports.io/games?date=DATE",
        "host": "v2.nba.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nba",
        "index": "teams",
        "url": "https://v2.nba.api-sports.io/teams",
        "host": "v2.nba.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nba",
        "index": "players",
        "url": "https://v2.nba.api-sports.io/players?country=USA",
        "host": "v2.nba.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "leagues",
        "url": "https://v1.american-football.api-sports.io/leagues",
        "host": "v1.american-football.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "teams",
        "url": "https://v1.american-football.api-sports.io/teams?season=2024&league=2",
        "host": "v1.american-football.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "games",
        "url": "https://v1.american-football.api-sports.io/games?date=DATE",
        "host": "v1.american-football.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "countries",
        "url": "https://v1.rugby.api-sports.io/countries",
        "host": "v1.rugby.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "leagues",
        "url": "https://v1.rugby.api-sports.io/leagues",
        "host": "v1.rugby.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "teams",
        "url": "https://v1.rugby.api-sports.io/teams?country=USA",
        "host": "v1.rugby.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "games",
        "url": "https://v1.rugby.api-sports.io/games?date=DATE",
        "host": "v1.rugby.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "countries",
        "url": "https://v1.volleyball.api-sports.io/countries",
        "host": "v1.volleyball.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "leagues",
        "url": "https://v1.volleyball.api-sports.io/leagues",
        "host": "v1.volleyball.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "teams",
        "url": "https://v1.volleyball.api-sports.io/teams?country=Ukraine",
        "host": "v1.volleyball.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "games",
        "url": "https://v1.volleyball.api-sports.io/games?date=DATE",
        "host": "v1.volleyball.api-sports.io",
        "frequency": 1  # Інтервал у хвилинах
    },
]
sports_dict = {
    "football": os.getenv("SASFOOTBALL"),
    "basketball": os.getenv("SASBASKETBALL"),
    "volleyball": os.getenv("SASVOLLEYBALL"),
    "afl": os.getenv("SASAFL"),
    "baseball": os.getenv("SASBASEBALL"),
    "formula-1": os.getenv("SASFORMULA1"),
    "handball": os.getenv("SASHANDBALL"),
    "hockey": os.getenv("SASHOCKEY"),
    "mma": os.getenv("SASMMA"),
    "nba":  os.getenv("SASNBA"),
    "nfl": os.getenv("SASNFL"),
    "rugby": os.getenv("SASRUGBY")
}
token_usage = {
    "football": 0,
    "basketball": 0,
    "volleyball": 0,
    "afl": 0,
    "baseball": 0,
    "formula-1": 0,
    "handball": 0,
    "hockey": 0,
    "mma": 0,
    "nba": 0,
    "nfl": 0,
    "rugby": 0
}

def auto_request_system(api: Dict[str, str]) -> None:
    try:
        global current_key_index
        print(f"Виконання запиту для {api['name']}, {api['index']}")
        today = datetime.now().strftime('%Y-%m-%d')
        url_with_date = api["url"].replace("DATE", today)
        if token_usage[api['name']] >= 99:
            current_key_index = (current_key_index + 1) % len(api_key)
            token_usage[api['name']] = 0
        token_usage[api['name']] += 1
        headers = {
            'x-rapidapi-host': api["host"],
            'x-rapidapi-key': api_key[current_key_index]
        }
        response = requests.get(url_with_date, headers=headers, timeout=10)
        response.raise_for_status()
        json_data = response.json()

        # Збереження у Blob Storage
        selected_sport = api["name"]
        key = sports_dict[selected_sport]
        blob_service_client = BlobServiceClient(account_url=account_url, credential=key)
        container_client = blob_service_client.get_container_client(api["name"])
        blob_name = f"{api['index'].replace(' ', '_').lower()}.json"
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(json.dumps(json_data), overwrite=True)
        print(f"JSON успішно збережено в Blob Storage як {blob_name}.")

    except requests.exceptions.RequestException as e:
        print(f"Помилка при запиті до {api['name']}: {e}")
    except Exception as e:
        print(f"Загальна помилка при збереженні даних для {api['name']}: {e}")





'''

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': api_key
    }

conn.request("GET", "/fixtures?live=all", headers=headers)
res = conn.getresponse()
data = res.read()
json_data = json.loads(data.decode("utf-8"))
print(json_data)

blob_service_client = BlobServiceClient(account_url=account_url, credential=sas_token)


container_client = blob_service_client.get_container_client("apidata")
blob_name = "sport_data.json"  # Унікальний індекс для блоба. Можна запит апішки за нього брати
blob_client = container_client.get_blob_client(blob_name)
blob_client.upload_blob(json.dumps(json_data), overwrite=True)
print("JSON успішно збережено в Blob Storage.")

# Додавання унікальних значень ключів до основної бд
with psycopg.connect("dbname=your_db user=your_user password=your_password") as db_connection:
    with db_connection.cursor() as cursor:
        cursor.execute("UPDATE sports SET blob_index = %s WHERE sport_name = %s", (blob_name, 'назва_виду_спорту'))
    db_connection.commit()
print("Інформацію успішно збережено.")

# Читання без проміжного ключа
container_client = blob_service_client.get_container_client("apidata")
blob_client = container_client.get_blob_client("fixtures-live=all.json")
blob_data = blob_client.download_blob()
json_data = blob_data.readall().decode("utf-8")
print(json_data)

# Отримання індекса блоба з бд
sport_name = 'sport_name'
with psycopg.connect("dbname=your_db user=your_user password=your_password") as db_connection:
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT blob_index FROM sports WHERE sport_name = %s", (sport_name,))
        blob_index = cursor.fetchone()[0]

# Завантаження JSON з Blob Storage
blob_service_client = BlobServiceClient(account_url=account_url, credential=sas_token)
container_client = blob_service_client.get_container_client("apidata")
blob_client = container_client.get_blob_client(blob_index)

blob_data = blob_client.download_blob()
json_data = blob_data.readall().decode("utf-8")

# Виведення результату
print(json_data)
'''