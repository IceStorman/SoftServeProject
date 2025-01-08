from datetime import datetime
from typing import Dict

from marshmallow import Schema, fields, pre_load


class BaseDTO(Schema):
    @pre_load
    def check_min_value(self, data, **kwargs):
        for field in data:
            if isinstance(data[field], int) and data[field] < 0:
                data[field] = None
        return data

    @pre_load
    def clean_letter(self, data, **kwargs):
        if 'letter' in data and data['letter']:
            data['letter'] = ' '.join(data['letter'].split()).lower()
        return data


class TeamsLeagueDTO(BaseDTO):
    teams__sport_id = fields.Int(required=False, missing=None)
    leagues__api_id = fields.Int(required=False, missing=None)
    countries__api_id = fields.Int(required=False, missing=None)
    page = fields.Int(required=False, missing=0)
    per_page = fields.Int(required=False, missing=0)

class TeamsStatisticsOrPlayersDTO(BaseDTO):
    sport_id = fields.Int(required=False, missing=None)
    team_id = fields.Int(required=False, missing=None)
    league_id = fields.Int(required=False, missing=None)


class SearchDTO(BaseDTO):
    leagues__sport_id = fields.Int(required=False, missing=None)
    countries__country_id = fields.Int(required=False, missing=None)
    letter = fields.Str(required=False, missing="")
    page = fields.Int(required=False, missing=0)
    per_page = fields.Int(required=False, missing=0)


class SportsLeagueDTO(BaseDTO):
    leagues__sport_id = fields.Int(required=False, missing=None)
    page = fields.Int(required=False, missing=0)
    per_page = fields.Int(required=False, missing=0)


class GamesDTO(BaseDTO):
    games__sport_id = fields.Int(required=False, missing=None)
    games__league_id = fields.Int(required=False, missing=None)
    games__country_id = fields.Int(required=False, missing=None)
    status = fields.Str(required=False, missing=None)
    games__date = fields.Date(required=False, missing=datetime.now().strftime('%Y-%m-%d'))
    page = fields.Int(required=False, missing=0)
    per_page = fields.Int(required=False, missing=0)


