import json
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from exept.exeptions import SportNotFoundError, DatabaseConnectionError
from api.routes.scripts import get_error_response
from service.api_logic.scripts import get_sport_by_name
from sqlalchemy.exc import OperationalError

TEAMS_JSON = "teams.json"
TEAM_KEY = "team"
DATA_KEY = "data"
SPORT_KEY = "sport"
RESPONSE_KEY = "response"

def get_teams(session):
    try:
        blob_indexes = get_all_blob_indexes_from_db(session, TEAMS_JSON)
        result = get_blob_data_for_all_sports(session, blob_indexes)
        data = json.loads(result)
        filtered_data = []

        for teams_data in data:
            processed_data = process_blob_data(teams_data)
            if processed_data:
                filtered_data.append(processed_data)
        return filtered_data, 200
    except OperationalError:
        raise DatabaseConnectionError()
    except Exception:
        raise Exception


def process_blob_data(sport_data):
    team = sport_data.get(DATA_KEY, {}).get(RESPONSE_KEY, [])
    sport = sport_data.get(SPORT_KEY)
    if team:
        return {
            SPORT_KEY: sport,
            TEAM_KEY: team,
        }
    return None


def get_teams_sport(session, sport_type):
    try:
        sport = get_sport_by_name(session, sport_type)
    except SportNotFoundError as e:
        return get_error_response({"error": e.message}, 404)
    try:
        blob_indexes = get_all_blob_indexes_from_db(session, TEAMS_JSON)
        result = get_blob_data_for_all_sports(session, blob_indexes)
        data = json.loads(result)
        filtered_data = []
        for teams_data in data:
            if sport_type == teams_data.get(SPORT_KEY):
                processed_data = process_blob_data(teams_data)
                if processed_data:
                    filtered_data.append(processed_data)
        return filtered_data, 200
    except OperationalError:
        raise DatabaseConnectionError()
    except Exception:
        raise Exception


"-------------------TEST--------------------"
from database.models import TeamIndex, Sport
from flask import Response

def get_teams1(session):
    try:
        teams = session.query(TeamIndex).join(Sport).all()
        filtered_data = []
        for team in teams:
            filtered_data.append({
                SPORT_KEY: team.sport.sport_name,
                TEAM_KEY: {
                    "name": team.name,
                    "logo": team.logo,
                    "api_id": team.api_id
                }
            })
        return filtered_data, 200
    except Exception:
        raise Exception


def get_teams_sport1(session, sport_type):
    try:
        sport = get_sport_by_name(session, sport_type)
    except SportNotFoundError as e:
        return get_error_response({"error": e.message}, 404)
    try:
        teams = session.query(TeamIndex).join(Sport).filter(Sport.sport_name == sport_type).all()
        filtered_data = []
        for team in teams:
            filtered_data.append({
                SPORT_KEY: team.sport.sport_name,
                TEAM_KEY: {
                    "name": team.name,
                    "logo": team.logo,
                    "api_id": team.api_id
                }
            })

        return filtered_data, 200
    except Exception:
        raise Exception


'''
from typing import Optional
from database.models import SportIndex, BlobIndex, Games, Country, TeamIndex, League

def fetch_teams(
        session,
        sport_id: Optional[int] = None,
        league_id: Optional[int] = None,
        country_id: Optional[int] = None,
        limit: Optional[int] = None
):
    query = session.query(TeamIndex)

    filters = []
    if sport_id is not None or "Unknown":
        filters.append(TeamIndex.sport_id == sport_id)
    if league_id is not None or "Unknown":
        filters.append(TeamIndex.league_id == league_id)
    if country_id is not None or "Unknown":
        filters.append(TeamIndex.country_id == country_id)

    # Застосовуємо фільтри до запиту
    if filters:
        query = query.filter(*filters)
    if limit is not None:
        query = query.limit(limit)

    teams = query.all()
    results = [
        {
            "sport_name": team.sport_name,
            "league_name": team.league_name,
            "country_name": team.country_name,
            "team_name": team.name,
        }
        for team in teams
    ]
    return Response(
        json.dumps(results, ensure_ascii=False),
        content_type='application/json; charset=utf-8',
        status=200
    )


def get_teams2(session, count, sport_id=None, league_id=None, country_id=None):
    try:
        session.execute(text("SELECT 1"))
        session.commit()
    except OperationalError:
        raise DatabaseConnectionError()
    except Exception:
        raise Exception
    teams = fetch_teams(
        session,
        limit=count,
        sport_id=sport_id,
        league_id=league_id,
        country_id=country_id
    )
    return teams
'''