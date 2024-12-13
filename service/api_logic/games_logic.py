from flask import Response
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from datetime import datetime
from typing import Optional
from database.models import SportIndex, BlobIndex, Games, Country, TeamIndex, League
from exept.exeptions import InvalidDateFormatError, SportNotFoundError
from exept.colors_text import print_error_message
from service.api_logic.scripts import get_sport_by_name
from api.routes.scripts import get_error_response
from sqlalchemy.orm import aliased
import json


GAMES_JSON = "games.json"
FIXTURES_JSON = "fixtures.json"
DATE_KEY = "date"
FIXTURE_KEY = "fixture"
DATA_KEY = "data"
RESPONSE_KEY = "response"
MATCHES_KEY = "matches"
FIXTURES_KEY = "fixtures"


def filter_matches_by_date(matches, today, date_key=DATE_KEY):
    today_matches = []
    for match in matches:
        match_date = match
        for key in date_key.split('.'):
            match_date = match_date.get(key, {})
        if match_date and isinstance(match_date, str):
            try:
                if datetime.fromisoformat(match_date).date() == today:
                    today_matches.append(match)
            except ValueError:
                error = InvalidDateFormatError(match_date)
                print(f"Warning: {error}")
                continue
    return today_matches



def process_blob_data(sport_data, today):
    blob_name = sport_data.get("blob_name")
    if blob_name == GAMES_JSON:
        matches = sport_data.get(DATA_KEY, {}).get(RESPONSE_KEY, [])
        today_matches = filter_matches_by_date(matches, today)
        if today_matches:
            return {
                "sport": sport_data.get("sport"),
                "blob_name": blob_name,
                MATCHES_KEY: today_matches,
            }
    elif blob_name == FIXTURES_JSON:
        fixtures = sport_data.get(DATA_KEY, {}).get(RESPONSE_KEY, [])
        today_matches = filter_matches_by_date(
            fixtures, today, date_key=f"{FIXTURE_KEY}.{DATE_KEY}"
        )
        if today_matches:
            return {
                "sport": sport_data.get("sport"),
                "blob_name": blob_name,
                FIXTURES_KEY: today_matches,
            }
    return None


def get_stream_info_today(session):
    blob_indexes = get_all_blob_indexes_from_db(session, GAMES_JSON) + \
                   get_all_blob_indexes_from_db(session, FIXTURES_JSON)
    result = get_blob_data_for_all_sports(session, blob_indexes)
    today = datetime.now().date()
    data = json.loads(result)
    filtered_data = []

    for sport_data in data:
        processed_data = process_blob_data(sport_data, today)
        if processed_data:
            filtered_data.append(processed_data)
    return filtered_data, 200


def get_stream_info_for_sport(session, sport_name):
    try:
        sport = get_sport_by_name(session, sport_name)
    except SportNotFoundError as e:
        print_error_message({"error": e.message})
        return get_error_response({"error": e.message },404)
    blob_indexes = (
        session.query(BlobIndex)
        .join(SportIndex, SportIndex.index_id == BlobIndex.sports_index_id)
        .filter(SportIndex.sport_id == sport.sport_id)
        .all()
    )
    result = get_blob_data_for_all_sports(session, blob_indexes)
    today = datetime.now().date()
    data = json.loads(result)
    filtered_data = []

    for sport_data in data:
        processed_data = process_blob_data(sport_data, today)
        if processed_data:
            processed_data["sport"] = sport_name  # Додати назву спорту
            filtered_data.append(processed_data)
    return filtered_data, 200

"-----------------TEST---------------------"
def fetch_games(
        session,
        sport_id: Optional[int] = None,
        league_id: Optional[int] = None,
        country_id: Optional[int] = None,
        status: Optional[str] = None,
        date: Optional[str] = None,
        limit: Optional[int] = None
):

    query = (
        session.query(
            Games.game_id,
            Games.status,
            Games.date,
            Games.time,
            Games.score_away_team,
            Games.score_home_team,
            League.name.label("league_name"),
            Country.name.label("country_name"),
            TeamIndex.name.label("home_team_name"),
            TeamIndex.logo.label("home_team_logo"),
            TeamIndex.name.label("away_team_name"),
            TeamIndex.logo.label("home_team_logo"),
        )
        .join(League, Games.league_id == League.league_id)
        .join(Country, Games.country_id == Country.country_id)
        .join(TeamIndex, Games.team_home_id == TeamIndex.team_index_id)
        .join(TeamIndex, Games.team_away_id == TeamIndex.team_index_id)
    )
    filters = []
    if sport_id is not None:
        filters.append(Games.sport_id == sport_id)
    if league_id is not None:
        filters.append(Games.league_id == league_id)
    if country_id is not None:
        filters.append(Games.country_id == country_id)
    if status is not None:
        filters.append(Games.status == status)
    if date is not None:
        filters.append(Games.date == date)

    # Застосовуємо фільтри до запиту
    if filters:
        query = query.filter(*filters)
    if limit is not None:
        query = query.limit(limit)

    games = query.all()
    results = [
        {
            "game_id": game.game_id,
            "status": game.status,
            "date": game.date,
            "time": game.time,
            "sport_name": game.sport_name,
            "league_name": game.league_name,
            "country_name": game.country_name,
            "home_team_name": game.home_team_name,
            "home_team_logo": game.home_team_logo,
            "away_team_name": game.away_team_name,
            "away_team_logo": game.home_team_logo,
            "home_score": game.score_home_team,
            "away_score": game.score_away_team,
        }
        for game in games
    ]
    return Response(
        json.dumps(results, ensure_ascii=False),
        content_type='application/json; charset=utf-8',
        status=200
    )


def get_games_today(session, count, sport_name=None, league=None, country=None):
    news = fetch_games(
        session,
        limit=count,
        sport_id=sport_name,
        league_id=league,
        country_id=country
    )
    return news
