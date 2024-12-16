from flask import Response
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from datetime import datetime
from typing import Optional
from database.models import SportIndex, BlobIndex, Games, Country, TeamIndex, League
from exept.exeptions import InvalidDateFormatError, SportNotFoundError
from exept.colors_text import print_error_message
from service.api_logic.scripts import get_sport_by_name
from api.routes.scripts import get_error_response
from exept.handle_exeptions import code_status

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


@code_status
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
    return filtered_data


@code_status
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
            processed_data["sport"] = sport_name
            filtered_data.append(processed_data)
    return filtered_data

