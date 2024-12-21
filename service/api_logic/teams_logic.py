import json
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from service.api_logic.scripts import get_sport_by_name
from api.routes.dto import TeamsLeagueDTO
from exept.handle_exeptions import handle_exceptions
from database.models import TeamIndex, Sport
from flask import Response


# TEAMS_JSON = "teams.json"
# TEAM_KEY = "team"
# DATA_KEY = "data"
# SPORT_KEY = "sport"
# RESPONSE_KEY = "response"
#
#
# @handle_exceptions
# def get_teams(session):
#     teams_blob_indexes = get_all_blob_indexes_from_db(session, TEAMS_JSON)
#     sport_result = get_blob_data_for_all_sports(session, teams_blob_indexes)
#     sport_result_json = json.loads(sport_result)
#     filtered_data = [
#         processed_data
#         for teams_data in sport_result_json
#         if (processed_data := process_blob_data(teams_data))
#     ]
#     return filtered_data
#
#
#
# @handle_exceptions
# def process_blob_data(sport_data):
#     team = sport_data.get(DATA_KEY, {}).get(RESPONSE_KEY, [])
#     sport = sport_data.get(SPORT_KEY)
#     if team:
#         return {
#             SPORT_KEY: sport,
#             TEAM_KEY: team,
#         }
#     return None
#
# @handle_exceptions
# def get_teams_sport(session, dto: TeamsLeagueDTO):
#
#         sport = get_sport_by_name(session, dto.sport)
#
#         teams_by_sport_blob_indexes = get_all_blob_indexes_from_db(session, TEAMS_JSON)
#         result = get_blob_data_for_all_sports(session, teams_by_sport_blob_indexes)
#         data = json.loads(result)
#
#         filtered_data = [
#             processed_data
#             for teams_data in data
#             if dto.sport == teams_data.get(SPORT_KEY) and (processed_data := process_blob_data(teams_data))
#         ]
#         return filtered_data


from service.api_logic.scripts import apply_filters
from api.routes.dto import TeamsLeagueOutputDTO
from sqlalchemy.orm import aliased
from typing import Optional
from database.models import Games, TeamIndex

@handle_exceptions
def get_teams(
        session,
        filters_dto: TeamsLeagueDTO
):
    query = session.query(TeamIndex)

    model_aliases = {
        "teams": TeamIndex,
    }

    query = apply_filters(query, filters_dto.to_dict(), model_aliases)

    offset, limit = filters_dto.get_pagination()

    if offset is not None and limit is not None:
        query = query.offset(offset).limit(limit)

    games = query.all()
    return [
        TeamsLeagueOutputDTO(
            league_name=team.league_name,
            country_name=team.country_name,
            team_name=team.name,
        ).to_dict() for team in teams
    ]





