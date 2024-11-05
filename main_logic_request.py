from azure.storage.blob import BlobClient
from azure.storage.blob import BlobServiceClient
import json
import http.client
import psycopg
import os
from dotenv import load_dotenv
import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler
from concurrent.futures import ThreadPoolExecutor

load_dotenv()
sas_token = os.getenv("SASTOKEN")
api_key = os.getenv("APIKEY")
account_url = os.getenv("BLOBURL")
sas_football = os.getenv("SASFOOTBALL")
sas_afl = os.getenv("SASAFL")
sas_baseball = os.getenv("SASBASEBALL")
sas_basketball = os.getenv("SASBASKETBALL")
sas_formula1 = os.getenv("SASFORMULA1")
sas_handball = os.getenv("SASHANDBALL")
sas_hockey = os.getenv("SASHOCKEY")
sas_mma = os.getenv("SASMMA")
sas_nba = os.getenv("SASNBA")
sas_nfl = os.getenv("SASNFL")
sas_rugby = os.getenv("SASRUGBY")
sas_volleyball = os.getenv("SASVOLLEYBALL")

apis = [
    {
        "name": "football",
        "index": "fixtures?live=all",
        "url": "https://v3.football.api-sports.io/fixtures?live=all",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "fixtures-rounds?season=2019&league=61",
        "url": "https://v3.football.api-sports.io/fixtures/rounds?season=2019&league=61",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "fixtures-headtohead?h2h=33-34",
        "url": "https://v3.football.api-sports.io/fixtures/headtohead?h2h=33-34",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "fixtures-statistics?fixture=215662&team=463",
        "url": "https://v3.football.api-sports.io/fixtures/statistics?fixture=215662&team=463",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "fixtures-events?fixture=215662",
        "url": "https://v3.football.api-sports.io/fixtures/events?fixture=215662",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "fixtures-lineups?fixture=592872",
        "url": "https://v3.football.api-sports.io/fixtures/lineups?fixture=592872",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "fixtures-players?fixture=169080",
        "url": "https://v3.football.api-sports.io/fixtures/players?fixture=169080",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "widgets-Games",
        "url": "https://v3.football.api-sports.io/widgets/Games",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "widgets-game",
        "url": "https://v3.football.api-sports.io/widgets/game",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "widgets-standings",
        "url": "https://v3.football.api-sports.io/widgets/standings",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "timezone",
        "url": "https://v3.football.api-sports.io/timezone",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "countries",
        "url": "https://v3.football.api-sports.io/countries",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "leagues",
        "url": "https://v3.football.api-sports.io/leagues",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "leagues-seasons",
        "url": "https://v3.football.api-sports.io/leagues/seasons",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "teams?id=33",
        "url": "https://v3.football.api-sports.io/teams?id=33",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "teams-statistics?season=2019&team=33&league=39",
        "url": "https://v3.football.api-sports.io/teams/statistics?season=2019&team=33&league=39",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "teams-seasons?team=33",
        "url": "https://v3.football.api-sports.io/teams/seasons?team=33",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "teams-countries",
        "url": "https://v3.football.api-sports.io/teams/countries",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "venues?id=556",
        "url": "https://v3.football.api-sports.io/venues?id=556",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "standings?league=39&season=2019",
        "url": "https://v3.football.api-sports.io/standings?league=39&season=2019",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "injuries?fixture=686314",
        "url": "https://v3.football.api-sports.io/injuries?fixture=686314",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "predictions?fixture=198772",
        "url": "https://v3.football.api-sports.io/predictions?fixture=198772",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "coachs?team=85",
        "url": "https://v3.football.api-sports.io/coachs?team=85",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "players-seasons",
        "url": "https://v3.football.api-sports.io/players/seasons",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "players-profiles?player=276",
        "url": "https://v3.football.api-sports.io/players/profiles?player=276",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "players?id=276&season=2019",
        "url": "https://v3.football.api-sports.io/players?id=276&season=2019",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "players-squads?team=33",
        "url": "https://v3.football.api-sports.io/players/squads?team=33",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "players-teams?player=276",
        "url": "https://v3.football.api-sports.io/players/teams?player=276",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "players-topscorers?season=2018&league=61",
        "url": "https://v3.football.api-sports.io/players/topscorers?season=2018&league=61",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "players-topassists?season=2020&league=61",
        "url": "https://v3.football.api-sports.io/players/topassists?season=2020&league=61",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "players-topyellowcards?season=2020&league=61",
        "url": "https://v3.football.api-sports.io/players/topyellowcards?season=2020&league=61",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "players-topredcards?season=2020&league=61",
        "url": "https://v3.football.api-sports.io/players/topredcards?season=2020&league=61",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "transfers?player=35845",
        "url": "https://v3.football.api-sports.io/transfers?player=35845",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "trophies?player=276",
        "url": "https://v3.football.api-sports.io/trophies?player=276",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "sidelined?player=276",
        "url": "https://v3.football.api-sports.io/sidelined?player=276",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "odds-live?bet=1&league=39",
        "url": "https://v3.football.api-sports.io/odds/live?bet=1&league=39",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "odds-bets",
        "url": "https://v3.football.api-sports.io/odds/bets",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "odds?season=2019&bet=1&bookmaker=6&fixture=157140&league=39",
        "url": "https://v3.football.api-sports.io/odds?season=2019&bet=1&bookmaker=6&fixture=157140&league=39",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "odds-mapping",
        "url": "https://v3.football.api-sports.io/odds/mapping",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "odds-bookmakers",
        "url": "https://v3.football.api-sports.io/odds/bookmakers",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },


]
sports_dict = {
    "football": sas_football,
    "basketball": sas_basketball,
    "volleyball": sas_volleyball,
    "afl": sas_afl,
    "baseball": sas_baseball,
    "formula1": sas_formula1,
    "handball": sas_handball,
    "hockey": sas_hockey,
    "mma": sas_mma,
    "nba": sas_nba,
    "nfl": sas_nfl,
    "rugby": sas_rugby
}
def fetch_and_store(api):
    try:
        print(f"Виконання запиту для {api['name']}")
        response = requests.get(api["url"], headers=api["headers"], timeout=10)
        response.raise_for_status()
        json_data = response.json()

        # Збереження у Blob Storage
        selected_sport = api["name"]
        if selected_sport in sports_dict:
            key = sports_dict[selected_sport]
        blob_service_client = BlobServiceClient(account_url=account_url, credential=key)
        container_client = blob_service_client.get_container_client(api["name"])
        blob_name = f"{api['index'].replace(' ', '_').lower()}.json"
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(json.dumps(json_data), overwrite=True)
        print(f"JSON успішно збережено в Blob Storage як {blob_name}.")

    except requests.exceptions.RequestException as e:
        print(f"Помилка при запиті до {api['name']}: {e}")



# Ініціалізація планувальника та пулу потоків
scheduler = BackgroundScheduler()
executor = ThreadPoolExecutor(max_workers=3)

# Додавання запланованих завдань для кожного API
for api in apis:
    print(f"Додаємо завдання для {api['index']} з частотою {api['frequency']} хвилин.")
    scheduler.add_job(
        fetch_and_store,
        'interval',
        minutes=api["frequency"],
        misfire_grace_time=300,
        args = [api]
    )


# Запуск планувальника
if __name__ == "__main__":
    scheduler.start()
    print("Планувальник запущено. Натисніть Ctrl+C для зупинки.")

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        executor.shutdown(wait=True)
        print("Планувальник зупинено.")



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