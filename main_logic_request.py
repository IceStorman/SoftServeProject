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


    {
        "name": "аfl",
        "index": "afl-timezone",
        "url": "https://v1.afl.api-sports.io/afl/timezone",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },


    {
        "name": "afl",
        "index": "afl-seasons",
        "url": "https://v1.afl.api-sports.io/afl/seasons",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-leagues",
        "url": "https://v1.afl.api-sports.io/afl/leagues",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-teams",
        "url": "https://v1.afl.api-sports.io/afl/teams",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-teams-statistics?id=1&season=2023",
        "url": "https://v1.afl.api-sports.io/afl/teams/statistics?id=1&season=2023",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-players?season=2023&team=1",
        "url": "https://v1.afl.api-sports.io/afl/players?season=2023&team=13",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-players-statistics?id=3&season=2023",
        "url": "https://v1.afl.api-sports.io/afl/players/statistics?id=3&season=2023",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-games?date=2022-09-01",
        "url": "https://v1.afl.api-sports.io/afl/games?date=2022-09-01",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-games-quarters?id=2515",
        "url": "https://v1.afl.api-sports.io/afl/games/quarters?id=2515",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-games-events?id=2515",
        "url": "https://v1.afl.api-sports.io/afl/games/events?id=2515",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-games-statistics-teams?id=2515",
        "url": "https://v1.afl.api-sports.io/afl/games/statistics/teams?id=2515",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-games-statistics-players?id=2515",
        "url": "https://v1.afl.api-sports.io/afl/games/statistics/players?id=2515",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-standings?season=2023&league=1",
        "url": "https://v1.afl.api-sports.io/afl/standings?season=2023&league=1",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-odds?game=2742&bookmaker=1",
        "url": "https://v1.afl.api-sports.io/afl/odds?game=2742&bookmaker=1",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-odds-bookmakers",
        "url": "https://v1.afl.api-sports.io/afl/odds/bookmakers",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "timezone",
        "url": "https://v1.baseball.api-sports.io/timezone",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "seasons",
        "url": "https://v1.baseball.api-sports.io/seasons",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "countries",
        "url": "https://v1.baseball.api-sports.io/countries",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "leagues",
        "url": "https://v1.baseball.api-sports.io/leagues",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "teams?id=3",
        "url": "https://v1.baseball.api-sports.io/teams?id=3",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "teams-statistics?league=1&season=2019&team=5",
        "url": "https://v1.baseball.api-sports.io/teams/statistics?league=1&season=2019&team=5",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "standings?league=1&season=2020&team=5",
        "url": "https://v1.baseball.api-sports.io/standings?league=1&season=2020&team=5",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "standings-stages?league=1&season=2020",
        "url": "https://v1.baseball.api-sports.io/standings/stages?league=1&season=2020",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "standings-groups?league=1&season=2020",
        "url": "https://v1.baseball.api-sports.io/sstandings/groups?league=1&season=2020",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "games?id=59647",
        "url": "https://v1.baseball.api-sports.io/games?id=59647",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "games-h2h?h2h=5-6&date=2017-04-28",
        "url": "https://v1.baseball.api-sports.io/games/h2h?h2h=5-6&date=2017-04-28",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "odds?game=5",
        "url": "https://v1.baseball.api-sports.io/odds?game=5",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "odds-bets",
        "url": "https://v1.baseball.api-sports.io/odds/bets",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "odds-bookmakers",
        "url": "https://v1.baseball.api-sports.io/odds/bookmakers",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "widgets-Games",
        "url": "https://v1.baseball.api-sports.io/widgets/Games",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "widgets-standings",
        "url": "https://v1.baseball.api-sports.io/widgets/standings",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "timezone",
        "url": "https://v1.basketball.api-sports.io/timezone",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "seasons",
        "url": "https://v1.basketball.api-sports.io/seasons",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "countries",
        "url": "https://v1.basketball.api-sports.io/countries",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "leagues",
        "url": "https://v1.basketball.api-sports.io/leagues",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "teams?id=139",
        "url": "https://v1.basketball.api-sports.io/teams?id=139",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "statistics?season=2019-2020&team=139&league=12",
        "url": "https://v1.basketball.api-sports.io/statistics?season=2019-2020&team=139&league=12",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "basketball-players?team=1&season=2023-2024",
        "url": "https://v1.basketball.api-sports.io/basketball/players?team=1&season=2023-2024",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "standings?league=12&season=2019-2020",
        "url": "https://v1.basketball.api-sports.io/standings?league=12&season=2019-2020",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "standings-stages",
        "url": "https://v1.basketball.api-sports.io/standings/stages",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "standings-groups",
        "url": "https://v1.basketball.api-sports.io/standings/groups",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "games?date=2019-11-23",
        "url": "https://v1.basketball.api-sports.io/games?date=2019-11-23",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "basketball-games-statistics-teams?id=391053",
        "url": "https://v1.basketball.api-sports.io/basketball/games/statistics/teams?id=391053",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "basketball-games-statistics-players?id=391053",
        "url": "https://v1.basketball.api-sports.io/basketball/games/statistics/players?id=391053",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "games?h2h=132-134",
        "url": "https://v1.basketball.api-sports.io/games?h2h=132-134",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "odds?season=2019-2020&bet=1&bookmaker=6&game=1912&league=12",
        "url": "https://v1.basketball.api-sports.io/odds?season=2019-2020&bet=1&bookmaker=6&game=1912&league=12",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "bookmakers",
        "url": "https://v1.basketball.api-sports.io/bookmakers",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "bets",
        "url": "https://v1.basketball.api-sports.io/bets",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "widgets-Games",
        "url": "https://v1.basketball.api-sports.io/widgets/Games",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "basketball",
        "index": "widgets-standings",
        "url": "https://v1.basketball.api-sports.io/widgets/standings",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
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
        print(f"Виконання запиту для {api['name']}, {api['index']}")
        response = requests.get(api["url"], headers=api["headers"], timeout=10)
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



# Ініціалізація планувальника та пулу потоків
scheduler = BackgroundScheduler()
executor = ThreadPoolExecutor(max_workers=3)

# Додавання запланованих завдань для кожного API
for api in apis:
    print(f"Додаємо завдання для {api['name']}, |||  {api['index']} з частотою {api['frequency']} хвилин.")
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