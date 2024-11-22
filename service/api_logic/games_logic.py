from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from datetime import datetime
from database.models import Sport, SportIndex, BlobIndex
import json


def get_stream_info_today(session):
    blob_indexes = get_all_blob_indexes_from_db(session, "games.json") + \
                   get_all_blob_indexes_from_db(session, "fixtures.json")
    result = get_blob_data_for_all_sports(session, blob_indexes)
    today = datetime.now().date()
    data = json.loads(result)
    filtered_data = []

    for sport_data in data:
        blob_name = sport_data.get("blob_name")

        if blob_name == "games.json":
            if 'data' in sport_data and 'response' in sport_data['data']:
                matches = sport_data['data']['response']
                today_matches = []
                for match in matches:
                    match_date = match.get('date')
                    if match_date and isinstance(match_date, str):
                        try:
                            if datetime.fromisoformat(match_date).date() == today:
                                today_matches.append(match)
                        except ValueError:
                            continue
                if today_matches:
                    filtered_data.append({
                        "sport": sport_data.get("sport"),
                        "blob_name": sport_data.get("blob_name"),
                        "matches": today_matches
                    })

        elif blob_name == "fixtures.json":
            if 'data' in sport_data and 'response' in sport_data['data']:
                matches = sport_data['data']['response']
                today_matches = []
                for fixture in matches:
                    fixture_date = fixture.get('fixture', {}).get('date')
                    if fixture_date and isinstance(fixture_date, str):
                        try:
                            if datetime.fromisoformat(fixture_date).date() == today:
                                today_matches.append(fixture)
                        except ValueError:
                            continue
                if today_matches:
                    filtered_data.append({
                        "sport": sport_data.get("sport"),
                        "blob_name": blob_name,
                        "fixtures": today_matches
                    })

    return filtered_data


def get_stream_info_for_sport(session, sport_name):
    sport = session.query(Sport).filter(Sport.sport_name == sport_name).first()
    if not sport:
        return {"error": f"Sport '{sport_name}' not found"}
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
        blob_name = sport_data.get("blob_name")

        if blob_name == "games.json":
            if 'data' in sport_data and 'response' in sport_data['data']:
                matches = sport_data['data']['response']
                today_matches = []
                for match in matches:
                    match_date = match.get('date')
                    if match_date and isinstance(match_date, str):
                        try:
                            if datetime.fromisoformat(match_date).date() == today:
                                today_matches.append(match)
                        except ValueError:
                            continue
                if today_matches:
                    filtered_data.append({
                        "sport": sport_name,
                        "blob_name": sport_data.get("blob_name"),
                        "matches": today_matches
                    })

        elif blob_name == "fixtures.json":
            if 'data' in sport_data and 'response' in sport_data['data']:
                matches = sport_data['data']['response']
                today_matches = []
                for fixture in matches:
                    fixture_date = fixture.get('fixture', {}).get('date')
                    if fixture_date and isinstance(fixture_date, str):
                        try:
                            if datetime.fromisoformat(fixture_date).date() == today:
                                today_matches.append(fixture)
                        except ValueError:
                            continue
                if today_matches:
                    filtered_data.append({
                        "sport": sport_name,
                        "blob_name": blob_name,
                        "fixtures": today_matches
                    })

    return filtered_data
