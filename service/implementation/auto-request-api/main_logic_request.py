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
from datetime import datetime

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
        "frequency": 5  # Інтервал у хвилинах
    },
    {
        "name": "football",
        "index": "fixtures-rounds?season&league",
        "url": "https://v3.football.api-sports.io/fixtures/rounds?season&league",
        "headers": {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1200  # Інтервал у хвилинах
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
        "url": "https://v1.afl.api-sports.io/timezone",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1 #1200  # Інтервал у хвилинах
    },


    {
        "name": "afl",
        "index": "afl-seasons",
        "url": "https://v1.afl.api-sports.io/seasons",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1 #1201  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-leagues",
        "url": "https://v1.afl.api-sports.io/leagues",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1 #1199  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-teams",
        "url": "https://v1.afl.api-sports.io/teams",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1 #600  # Інтервал у хвилинах
    },
            #маю знати id команди
            {
                "name": "afl",
                "index": "afl-teams-statistics",
                "url": "https://v1.afl.api-sports.io/teams/statistics?id=1&season=2023",
                "headers": {
                    'x-rapidapi-host': "v1.afl.api-sports.io",
                    'x-rapidapi-key': api_key
                },
                "frequency": 0.1 #1200  # Інтервал у хвилинах
            },
            #маю знати id команди щоб отримати список гравців в сезоні
            {
                "name": "afl",
                "index": "afl-players",
                "url": "https://v1.afl.api-sports.io/players?season=2023&team=13",
                "headers": {
                    'x-rapidapi-host': "v1.afl.api-sports.io",
                    'x-rapidapi-key': api_key
                },
                "frequency": 1 #1200  # Інтервал у хвилинах
            },
            #маю знати id спортсмена щоб отримати статистику конкретонго сезона
            {
                "name": "afl",
                "index": "afl-players-statistics",
                "url": "https://v1.afl.api-sports.io/players/statistics?id=3&season=2023",
                "headers": {
                    'x-rapidapi-host': "v1.afl.api-sports.io",
                    'x-rapidapi-key': api_key
                },
                "frequency": 1 #1200  # Інтервал у хвилинах
            },
    {
        "name": "afl",
        "index": "afl-games",
        "url": "https://v1.afl.api-sports.io/games?date=DATE",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1 #13  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-games-quarters?",
        "url": "https://v1.afl.api-sports.io/games/quarters?date=DATE",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1 #20  # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-games-events",
        "url": "https://v1.afl.api-sports.io/games/events?date=DATE",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1 #23  # Інтервал у хвилинах
    },
    #ID TEAM
    {
        "name": "afl",
        "index": "afl-games-statistics-teams",
        "url": "https://v1.afl.api-sports.io/games/statistics/teams?date=DATE",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1 #21 # Інтервал у хвилинах
    },
    {
        "name": "afl",
        "index": "afl-games-statistics-players",
        "url": "https://v1.afl.api-sports.io/games/statistics/players?date=DATE",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1 #22 # Інтервал у хвилинах
    },
            #маю знати id ліги та рік сезону
            {
                "name": "afl",
                "index": "afl-standings",
                "url": "https://v1.afl.api-sports.io/standings?season=2023&league=1",
                "headers": {
                    'x-rapidapi-host': "v1.afl.api-sports.io",
                    'x-rapidapi-key': api_key
                },
                "frequency": 1 #1200 # Інтервал у хвилинах
            },
            #маю знати id гри та букмекера
            {
                "name": "afl",
                "index": "afl-odds",
                "url": "https://v1.afl.api-sports.io/odds?game=2742",
                "headers": {
                    'x-rapidapi-host': "v1.afl.api-sports.io",
                    'x-rapidapi-key': api_key
                },
                "frequency": 1 #600 # Інтервал у хвилинах
            },
    {
        "name": "afl",
        "index": "afl-odds-bookmakers",
        "url": "https://v1.afl.api-sports.io/odds/bookmakers",
        "headers": {
            'x-rapidapi-host': "v1.afl.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1 #599 # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "timezone",
        "url": "https://v1.baseball.api-sports.io/timezone",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1 #1200 # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "seasons",
        "url": "https://v1.baseball.api-sports.io/seasons",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1 #1199 # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "countries",
        "url": "https://v1.baseball.api-sports.io/countries",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1 #1201 # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "leagues",
        "url": "https://v1.baseball.api-sports.io/leagues",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1 #1200 # Інтервал у хвилинах
    },
    {
        "name": "baseball",
        "index": "teams",
        "url": "https://v1.baseball.api-sports.io/teams",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1 #600 # Інтервал у хвилинах
    },
            #маю знати id команди
            {
                "name": "baseball",
                "index": "teams-statistics",
                "url": "https://v1.baseball.api-sports.io/teams/statistics?league=1&season=2019&team=5",
                "headers": {
                    'x-rapidapi-host': "v1.baseball.api-sports.io",
                    'x-rapidapi-key': api_key
                },
                "frequency": 1 #600 # Інтервал у хвилинах
            },
            # маю знати id ліги
            {
                "name": "baseball",
                "index": "standings",
                "url": "https://v1.baseball.api-sports.io/standings?league=1",
                "headers": {
                    'x-rapidapi-host': "v1.baseball.api-sports.io",
                    'x-rapidapi-key': api_key
                },
                "frequency": 1 #1198 # Інтервал у хвилинах
            },
            {
                "name": "baseball",
                "index": "standings-stages",
                "url": "https://v1.baseball.api-sports.io/standings/stages?league=1",
                "headers": {
                    'x-rapidapi-host': "v1.baseball.api-sports.io",
                    'x-rapidapi-key': api_key
                },
                "frequency": 1 #1197 # Інтервал у хвилинах
            },
            {
                "name": "baseball",
                "index": "standings-groups",
                "url": "https://v1.baseball.api-sports.io/sstandings/groups?league=1&season=2020",
                "headers": {
                    'x-rapidapi-host': "v1.baseball.api-sports.io",
                    'x-rapidapi-key': api_key
                },
                "frequency": 1 #1197 # Інтервал у хвилинах
            },
    {
        "name": "baseball",
        "index": "games",
        "url": "https://v1.baseball.api-sports.io/games",
        "headers": {
            'x-rapidapi-host': "v1.baseball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1 #15 # Інтервал у хвилинах
    },
            #маю знати h2h
            {
                "name": "baseball",
                "index": "games-h2h",
                "url": "https://v1.baseball.api-sports.io/games/h2h?h2h=5-6",
                "headers": {
                    'x-rapidapi-host': "v1.baseball.api-sports.io",
                    'x-rapidapi-key': api_key
                },
                "frequency": 1 #13 # Інтервал у хвилинах
            },
    #можливо id гри
    {
        "name": "baseball",
        "index": "odds",
        "url": "https://v1.baseball.api-sports.io/odds",
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
                #це для html
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
        "index": "teams",
        "url": "https://v1.basketball.api-sports.io/teams",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
            #маю знати лігу сезон команду
            {
                "name": "basketball",
                "index": "statistics",
                "url": "https://v1.basketball.api-sports.io/statistics?season=2019-2020&team=139&league=12",
                "headers": {
                    'x-rapidapi-host': "v1.basketball.api-sports.io",
                    'x-rapidapi-key': api_key
                },
                "frequency": 1  # Інтервал у хвилинах
            },
            #маю знати команду та сезони
            {
                "name": "basketball",
                "index": "basketball-players",
                "url": "https://v1.basketball.api-sports.io/basketball/players?team=1&season=2023-2024",
                "headers": {
                    'x-rapidapi-host': "v1.basketball.api-sports.io",
                    'x-rapidapi-key': api_key
                },
                "frequency": 1  # Інтервал у хвилинах
            },
            {
                "name": "basketball",
                "index": "standings0",
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
        "index": "games",
        "url": "https://v1.basketball.api-sports.io/games?date=DATE",
        "headers": {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
            #маю знати id команди
            {
                "name": "basketball",
                "index": "basketball-games-statistics-teams",
                "url": "https://v1.basketball.api-sports.io/basketball/games/statistics/teams?id=391053",
                "headers": {
                    'x-rapidapi-host': "v1.basketball.api-sports.io",
                    'x-rapidapi-key': api_key
                },
                "frequency": 1  # Інтервал у хвилинах
            },
    {
        "name": "basketball",
        "index": "basketball-games-statistics-players",
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
    {
        "name": "formula-1",
        "index": "timezone",
        "url": "https://v1.formula-1.api-sports.io/timezone",
        "headers": {
            'x-rapidapi-host': "v1.formula-1.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "formula-1",
        "index": "seasons",
        "url": "https://v1.formula-1.api-sports.io/seasons",
        "headers": {
            'x-rapidapi-host': "v1.formula-1.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "formula-1",
        "index": "competitions",
        "url": "https://v1.formula-1.api-sports.io/competitions",
        "headers": {
            'x-rapidapi-host': "v1.formula-1.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "formula-1",
        "index": "circuits",
        "url": "https://v1.formula-1.api-sports.io/circuits",
        "headers": {
            'x-rapidapi-host': "v1.formula-1.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "formula-1",
        "index": "teams",
        "url": "https://v1.formula-1.api-sports.io/teams",
        "headers": {
            'x-rapidapi-host': "v1.formula-1.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "formula-1",
        "index": "drivers?search=lewi",
        "url": "https://v1.formula-1.api-sports.io/drivers?search=lewi",
        "headers": {
            'x-rapidapi-host': "v1.formula-1.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "formula-1",
        "index": "races",
        "url": "https://v1.formula-1.api-sports.io/races?date=DATE",
        "headers": {
            'x-rapidapi-host': "v1.formula-1.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "formula-1",
        "index": "rankings-teams",
        "url": "https://v1.formula-1.api-sports.io/rankings/teams?season=2019",
        "headers": {
            'x-rapidapi-host': "v1.formula-1.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "formula-1",
        "index": "rankings-drivers",
        "url": "https://v1.formula-1.api-sports.io/rankings/drivers?season=2019",
        "headers": {
            'x-rapidapi-host': "v1.formula-1.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "formula-1",
        "index": "rankings-races",
        "url": "https://v1.formula-1.api-sports.io/rankings/races?race=50",
        "headers": {
            'x-rapidapi-host': "v1.formula-1.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "formula-1",
        "index": "rankings-fastestlaps",
        "url": "https://v1.formula-1.api-sports.io/rankings/fastestlaps?race=50",
        "headers": {
            'x-rapidapi-host': "v1.formula-1.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "formula-1",
        "index": "rankings-startinggrid",
        "url": "https://v1.formula-1.api-sports.io/rankings/startinggrid?race=50",
        "headers": {
            'x-rapidapi-host': "v1.formula-1.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "formula-1",
        "index": "pitstops",
        "url": "https://v1.formula-1.api-sports.io/pitstops?race=50",
        "headers": {
            'x-rapidapi-host': "v1.formula-1.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "handball",
        "index": "timezone",
        "url": "https://v1.handball.api-sports.io/timezone",
        "headers": {
            'x-rapidapi-host': "v1.handball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "handball",
        "index": "seasons",
        "url": "https://v1.handball.api-sports.io/seasons",
        "headers": {
            'x-rapidapi-host': "v1.handball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "handball",
        "index": "countries",
        "url": "https://v1.handball.api-sports.io/countries",
        "headers": {
            'x-rapidapi-host': "v1.handball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "handball",
        "index": "leagues",
        "url": "https://v1.handball.api-sports.io/leagues",
        "headers": {
            'x-rapidapi-host': "v1.handball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "handball",
        "index": "teams",
        "url": "https://v1.handball.api-sports.io/teams?country=Ukraine",
        "headers": {
            'x-rapidapi-host': "v1.handball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
            {
                "name": "handball",
                "index": "teams-statistics",
                "url": "https://v1.handball.api-sports.io/teams/statistics?season=2024&team=4450&league=1",
                "headers": {
                    'x-rapidapi-host': "v1.handball.api-sports.io",
                    'x-rapidapi-key': api_key
                },
                "frequency": 1  # Інтервал у хвилинах
            },
            {
                "name": "handball",
                "index": "standings",
                "url": "https://v1.handball.api-sports.io/standings?league=1&season=2024",
                "headers": {
                    'x-rapidapi-host': "v1.handball.api-sports.io",
                    'x-rapidapi-key': api_key
                },
                "frequency": 1  # Інтервал у хвилинах
            },
            {
                "name": "handball",
                "index": "standings-stages",
                "url": "https://v1.handball.api-sports.io/standings/stages?league=1&season=2024",
                "headers": {
                    'x-rapidapi-host': "v1.handball.api-sports.io",
                    'x-rapidapi-key': api_key
                },
                "frequency": 1  # Інтервал у хвилинах
            },
            {
                "name": "handball",
                "index": "standings-groups",
                "url": "https://v1.handball.api-sports.io/standings/groups?league=1&season=2024",
                "headers": {
                    'x-rapidapi-host': "v1.handball.api-sports.io",
                    'x-rapidapi-key': api_key
                },
                "frequency": 1  # Інтервал у хвилинах
            },
    {
        "name": "handball",
        "index": "games",
        "url": "https://v1.handball.api-sports.io/games?date=DATE",
        "headers": {
            'x-rapidapi-host': "v1.handball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
            {
                "name": "handball",
                "index": "games-h2h",
                "url": "https://v1.handball.api-sports.io/games/h2h?h2h=2662-2672",
                "headers": {
                    'x-rapidapi-host': "v1.handball.api-sports.io",
                    'x-rapidapi-key': api_key
                },
                "frequency": 0.1  # Інтервал у хвилинах
            },
    {
        "name": "handball",
        "index": "odds?game=4289",
        "url": "https://v1.handball.api-sports.io/odds?game=4289",
        "headers": {
            'x-rapidapi-host': "v1.handball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "handball",
        "index": "bets",
        "url": "https://v1.handball.api-sports.io/bets",
        "headers": {
            'x-rapidapi-host': "v1.handball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "handball",
        "index": "bookmakers",
        "url": "https://v1.handball.api-sports.io/bookmakers",
        "headers": {
            'x-rapidapi-host': "v1.handball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "handball",
        "index": "widgets-standings",
        "url": "https://v1.handball.api-sports.io/widgets/standings",
        "headers": {
            'x-rapidapi-host': "v1.handball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "handball",
        "index": "widgets-Games",
        "url": "https://v1.handball.api-sports.io/widgets/Games",
        "headers": {
            'x-rapidapi-host': "v1.handball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "timezone",
        "url": "https://v1.hockey.api-sports.io/timezone",
        "headers": {
            'x-rapidapi-host': "v1.hockey.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "widgets-Games",
        "url": "https://v1.hockey.api-sports.io/widgets/Games",
        "headers": {
            'x-rapidapi-host': "v1.hockey.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },










    {
        "name": "hockey",
        "index": "widgets-standings",
        "url": "https://v1.hockey.api-sports.io/widgets/standings",
        "headers": {
            'x-rapidapi-host': "v1.hockey.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "seasons",
        "url": "https://v1.hockey.api-sports.io/seasons",
        "headers": {
            'x-rapidapi-host': "v1.hockey.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "countries",
        "url": "https://v1.hockey.api-sports.io/countries",
        "headers": {
            'x-rapidapi-host': "v1.hockey.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "leagues",
        "url": "https://v1.hockey.api-sports.io/leagues",
        "headers": {
            'x-rapidapi-host': "v1.hockey.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "teams?id=119",
        "url": "https://v1.hockey.api-sports.io/teams?id=119",
        "headers": {
            'x-rapidapi-host': "v1.hockey.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "teams-statistics?season=2019&team=29&league=3",
        "url": "https://v1.hockey.api-sports.io/teams/statistics?season=2019&team=29&league=3",
        "headers": {
            'x-rapidapi-host': "v1.hockey.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "standings?league=3&season=2019",
        "url": "https://v1.hockey.api-sports.io/standings?league=3&season=2019",
        "headers": {
            'x-rapidapi-host': "v1.hockey.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "standings-stages",
        "url": "https://v1.hockey.api-sports.io/standings/stages",
        "headers": {
            'x-rapidapi-host': "v1.hockey.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "standings-groups",
        "url": "https://v1.hockey.api-sports.io/standings/groups",
        "headers": {
            'x-rapidapi-host': "v1.hockey.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "games?id=8279",
        "url": "https://v1.hockey.api-sports.io/games?id=8279",
        "headers": {
            'x-rapidapi-host': "v1.hockey.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "games-h2h?h2h=367-382",
        "url": "https://v1.hockey.api-sports.io/games/h2h?h2h=367-382",
        "headers": {
            'x-rapidapi-host': "v1.hockey.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "games-events?game=8279",
        "url": "https://v1.hockey.api-sports.io/games/events?game=8279",
        "headers": {
            'x-rapidapi-host': "v1.hockey.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "odds?bookmaker=1&game=11590",
        "url": "https://v1.hockey.api-sports.io/odds?bookmaker=1&game=11590",
        "headers": {
            'x-rapidapi-host': "v1.hockey.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "bets",
        "url": "https://v1.hockey.api-sports.io/bets",
        "headers": {
            'x-rapidapi-host': "v1.hockey.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "hockey",
        "index": "bookmakers",
        "url": "https://v1.hockey.api-sports.io/bookmakers",
        "headers": {
            'x-rapidapi-host': "v1.hockey.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "timezone",
        "url": "https://v1.mma.api-sports.io/timezone",
        "headers": {
            'x-rapidapi-host': "v1.mma.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "seasons",
        "url": "https://v1.mma.api-sports.io/seasons",
        "headers": {
            'x-rapidapi-host': "v1.mma.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "categories",
        "url": "https://v1.mma.api-sports.io/categories",
        "headers": {
            'x-rapidapi-host': "v1.mma.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "teams",
        "url": "https://v1.mma.api-sports.io/teams",
        "headers": {
            'x-rapidapi-host': "v1.mma.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "fighters?id=691",
        "url": "https://v1.mma.api-sports.io/fighters?id=691",
        "headers": {
            'x-rapidapi-host': "v1.mma.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "fighters-records?id=691",
        "url": "https://v1.mma.api-sports.io/fighters/records?id=691",
        "headers": {
            'x-rapidapi-host': "v1.mma.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "fighters-records?id=691",
        "url": "https://v1.mma.api-sports.io/fighters/records?id=691",
        "headers": {
            'x-rapidapi-host': "v1.mma.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "fights?date=2023-08-26",
        "url": "https://v1.mma.api-sports.io/fights?date=2023-08-26",
        "headers": {
            'x-rapidapi-host': "v1.mma.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "fights-results?ids=865-878-879",
        "url": "https://v1.mma.api-sports.io/fights/results?ids=865-878-879",
        "headers": {
            'x-rapidapi-host': "v1.mma.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "fights-statistics-fighters?id=879",
        "url": "https://v1.mma.api-sports.io/fights/statistics/fighters?id=879",
        "headers": {
            'x-rapidapi-host': "v1.mma.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "odds?fight=878",
        "url": "https://v1.mma.api-sports.io/odds?fight=878",
        "headers": {
            'x-rapidapi-host': "v1.mma.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "odds-bets",
        "url": "https://v1.mma.api-sports.io/odds/bets",
        "headers": {
            'x-rapidapi-host': "v1.mma.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "mma",
        "index": "odds-bookmakers",
        "url": "https://v1.mma.api-sports.io/odds/bookmakers",
        "headers": {
            'x-rapidapi-host': "v1.mma.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nba",
        "index": "seasons",
        "url": "https://v2.nba.api-sports.io/seasons",
        "headers": {
            'x-rapidapi-host': "v2.nba.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nba",
        "index": "leagues",
        "url": "https://v2.nba.api-sports.io/leagues",
        "headers": {
            'x-rapidapi-host': "v2.nba.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nba",
        "index": "games?date=2022-03-09",
        "url": "https://v2.nba.api-sports.io/games?date=2022-03-09",
        "headers": {
            'x-rapidapi-host': "v2.nba.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nba",
        "index": "games-statistics?id=10403",
        "url": "https://v2.nba.api-sports.io/games/statistics?id=10403",
        "headers": {
            'x-rapidapi-host': "v2.nba.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nba",
        "index": "teams?id=1",
        "url": "https://v2.nba.api-sports.io/teams?id=1",
        "headers": {
            'x-rapidapi-host': "v2.nba.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nba",
        "index": "teams-statistics?season=2020&id=1",
        "url": "https://v2.nba.api-sports.io/teams/statistics?season=2020&id=1",
        "headers": {
            'x-rapidapi-host': "v2.nba.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nba",
        "index": "players?id=265",
        "url": "https://v2.nba.api-sports.io/players?id=265",
        "headers": {
            'x-rapidapi-host': "v2.nba.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nba",
        "index": "players-statistics?season=2020&id=734",
        "url": "https://v2.nba.api-sports.io/players/statistics?season=2020&id=734",
        "headers": {
            'x-rapidapi-host': "v2.nba.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nba",
        "index": "standings?league=standard&season=2021",
        "url": "https://v2.nba.api-sports.io/standings?league=standard&season=2021",
        "headers": {
            'x-rapidapi-host': "v2.nba.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "timezone",
        "url": "https://v1.american-football.api-sports.io/timezone",
        "headers": {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "seasons",
        "url": "https://v1.american-football.api-sports.io/seasons",
        "headers": {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "leagues",
        "url": "https://v1.american-football.api-sports.io/leagues",
        "headers": {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "teams?id=1",
        "url": "https://v1.american-football.api-sports.io/teams?id=1",
        "headers": {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "players?id=1",
        "url": "https://v1.american-football.api-sports.io/players?id=1",
        "headers": {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "players-statistics?id=1&season=2022",
        "url": "https://v1.american-football.api-sports.io/players/statistics?id=1&season=2022",
        "headers": {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "injuries?player=53",
        "url": "https://v1.american-football.api-sports.io/injuries?player=53",
        "headers": {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "games?date=2022-09-30",
        "url": "https://v1.american-football.api-sports.io/games?date=2022-09-30",
        "headers": {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "games-events?id=1986",
        "url": "https://v1.american-football.api-sports.io/games/events?id=1986",
        "headers": {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "games-statistics-teams?id=1985",
        "url": "https://v1.american-football.api-sports.io/games/statistics/teams?id=1985",
        "headers": {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "games-statistics-players?id=1985",
        "url": "https://v1.american-football.api-sports.io/games/statistics/players?id=1985",
        "headers": {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "standings?league=1&season=2022",
        "url": "https://v1.american-football.api-sports.io/standings?league=1&season=2022",
        "headers": {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "standings-stages",
        "url": "https://v1.american-football.api-sports.io/standings/stages",
        "headers": {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "standings-divisions",
        "url": "https://v1.american-football.api-sports.io/standings/divisions",
        "headers": {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "odds?game=7532",
        "url": "https://v1.american-football.api-sports.io/odds?game=7532",
        "headers": {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "odds-bets",
        "url": "https://v1.american-football.api-sports.io/odds/bets",
        "headers": {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "nfl",
        "index": "odds-bookmakers",
        "url": "https://v1.american-football.api-sports.io/odds/bookmakers",
        "headers": {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "timezone",
        "url": "https://v1.rugby.api-sports.io/timezone",
        "headers": {
            'x-rapidapi-host': "v1.rugby.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "seasons",
        "url": "https://v1.rugby.api-sports.io/seasons",
        "headers": {
            'x-rapidapi-host': "v1.rugby.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "countries",
        "url": "https://v1.rugby.api-sports.io/countries",
        "headers": {
            'x-rapidapi-host': "v1.rugby.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "leagues",
        "url": "https://v1.rugby.api-sports.io/leagues",
        "headers": {
            'x-rapidapi-host': "v1.rugby.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "teams?id=119",
        "url": "https://v1.rugby.api-sports.io/teams?id=119",
        "headers": {
            'x-rapidapi-host': "v1.rugby.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "teams-statistics?season=2019&team=29&league=3",
        "url": "https://v1.rugby.api-sports.io/teams/statistics?season=2019&team=29&league=3",
        "headers": {
            'x-rapidapi-host': "v1.rugby.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "standings?league=3&season=2019",
        "url": "https://v1.rugby.api-sports.io/standings?league=3&season=2019",
        "headers": {
            'x-rapidapi-host': "v1.rugby.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "standings-stages",
        "url": "https://v1.rugby.api-sports.io/standings/stages",
        "headers": {
            'x-rapidapi-host': "v1.rugby.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "standings-groups",
        "url": "https://v1.rugby.api-sports.io/standings/groups",
        "headers": {
            'x-rapidapi-host': "v1.rugby.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "games?id=8279",
        "url": "https://v1.rugby.api-sports.io/games?id=8279",
        "headers": {
            'x-rapidapi-host': "v1.rugby.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "games-h2h?h2h=367-368",
        "url": "https://v1.rugby.api-sports.io/games/h2h?h2h=367-368",
        "headers": {
            'x-rapidapi-host': "v1.rugby.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "odds?game=1107",
        "url": "https://v1.rugby.api-sports.io/odds?game=1107",
        "headers": {
            'x-rapidapi-host': "v1.rugby.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "bets",
        "url": "https://v1.rugby.api-sports.io/bets",
        "headers": {
            'x-rapidapi-host': "v1.rugby.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "bookmakers",
        "url": "https://v1.rugby.api-sports.io/bookmakers",
        "headers": {
            'x-rapidapi-host': "v1.rugby.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "widgets-Games",
        "url": "https://v1.rugby.api-sports.io/widgets/Games",
        "headers": {
            'x-rapidapi-host': "v1.rugby.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "rugby",
        "index": "widgets-standings",
        "url": "https://v1.rugby.api-sports.io/widgets/standings",
        "headers": {
            'x-rapidapi-host': "v1.rugby.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "widgets-standings",
        "url": "https://v1.volleyball.api-sports.io/widgets/standings",
        "headers": {
            'x-rapidapi-host': "v1.volleyball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "widgets-Games",
        "url": "https://v1.volleyball.api-sports.io/widgets/Games",
        "headers": {
            'x-rapidapi-host': "v1.volleyball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "timezone",
        "url": "https://v1.volleyball.api-sports.io/timezone",
        "headers": {
            'x-rapidapi-host': "v1.volleyball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "seasons",
        "url": "https://v1.volleyball.api-sports.io/seasons",
        "headers": {
            'x-rapidapi-host': "v1.volleyball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "countries",
        "url": "https://v1.volleyball.api-sports.io/countries",
        "headers": {
            'x-rapidapi-host': "v1.volleyball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "leagues",
        "url": "https://v1.volleyball.api-sports.io/leagues",
        "headers": {
            'x-rapidapi-host': "v1.volleyball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "teams?id=119",
        "url": "https://v1.volleyball.api-sports.io/teams?id=119",
        "headers": {
            'x-rapidapi-host': "v1.volleyball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "teams-statistics?season=2019&team=1&league=1",
        "url": "https://v1.volleyball.api-sports.io/teams/statistics?season=2019&team=1&league=1",
        "headers": {
            'x-rapidapi-host': "v1.volleyball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "standings?league=3&season=2021",
        "url": "https://v1.volleyball.api-sports.io/standings?league=3&season=2021",
        "headers": {
            'x-rapidapi-host': "v1.volleyball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "standings-stages",
        "url": "https://v1.volleyball.api-sports.io/standings/stages",
        "headers": {
            'x-rapidapi-host': "v1.volleyball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "standings-groups",
        "url": "https://v1.volleyball.api-sports.io/standings/groups",
        "headers": {
            'x-rapidapi-host': "v1.volleyball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "games?id=8279",
        "url": "https://v1.volleyball.api-sports.io/games?id=8279",
        "headers": {
            'x-rapidapi-host': "v1.volleyball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "games-h2h?h2h=829-835",
        "url": "https://v1.volleyball.api-sports.io/games/h2h?h2h=829-835",
        "headers": {
            'x-rapidapi-host': "v1.volleyball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "odds?game=63367",
        "url": "https://v1.volleyball.api-sports.io/odds?game=63367",
        "headers": {
            'x-rapidapi-host': "v1.volleyball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "bets",
        "url": "https://v1.volleyball.api-sports.io/bets",
        "headers": {
            'x-rapidapi-host': "v1.volleyball.api-sports.io",
            'x-rapidapi-key': api_key
        },
        "frequency": 1  # Інтервал у хвилинах
    },
    {
        "name": "volleyball",
        "index": "bookmakers",
        "url": "https://v1.volleyball.api-sports.io/bookmakers",
        "headers": {
            'x-rapidapi-host': "v1.volleyball.api-sports.io",
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
    "formula-1": sas_formula1,
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
        today = datetime.now().strftime('%Y-%m-%d')
        url_with_date = api["url"].replace("DATE", today)

        response = requests.get(url_with_date, headers=api["headers"], timeout=10)
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