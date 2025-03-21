import re
from collections import namedtuple
from datetime import datetime
from marshmallow import Schema, fields, pre_load, post_load, ValidationError, EXCLUDE


class BaseDTO(Schema):
    class Meta:
        unknown = EXCLUDE

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

    @pre_load
    def to_lower(self, data, **kwargs):
        if 'auth_provider' in data and data['auth_provider']:
            data['auth_provider'] = data['auth_provider'].lower()
        return data

    @post_load
    def make_object(self, data, **kwargs):
        class_name = self.__class__.__name__.replace("Schema", "") or "DTO"
        return namedtuple(class_name, data.keys())(*data.values())

    @pre_load
    def validate_email(self, data, **kwargs):
        if 'email' in data:
            if not re.match(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', data['email']):
                raise ValidationError("Invalid email format", field_name="email")
        return data

    @pre_load
    def validate_username(self, data, **kwargs):
        if 'username' in data:
            regex = re.compile(r'[ @!#$%^&*()<>?/\|}{~:;,+=]')
            if regex.search(data['username']) or not data['username']:
                raise ValidationError("Invalid username format", field_name="username")
        return data

    @pre_load
    def validate_password(self, data, **kwargs):
        if 'password' in data:
            regex = re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?!.*\s){8,}')
            if not re.match(regex, data['password']):
                raise ValidationError("Invalid password format", field_name="password_hash")
        return data


class TeamsLeagueDTO(BaseDTO):
    sport_id = fields.Int(required=False, missing=None)
    league_id = fields.Int(required=False, missing=None)
    country_id = fields.Int(required=False, missing=None)
    name = fields.Str(required=False, missing=None)
    page = fields.Int(required=False, missing=0)
    per_page = fields.Int(required=False, missing=0)


class TeamsStatisticsOrPlayersDTO(BaseDTO):
    sport_id = fields.Int(required=False, missing=None)
    team_id = fields.Int(required=False, missing=None)
    league_id = fields.Int(required=False, missing=None)
    name = fields.Str(required=False, missing=None)


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


class NewsDTO(BaseDTO):
    news__news_id = fields.Int(required=False, missing=None)
    news__sport_id = fields.Int(required=False, missing=None)
    news__interest_rate = fields.Int(required=False, missing=None)


class StreamsDTO(BaseDTO):
    streams__stream_id = fields.Int(required=False, missing = None)
    streams__stream_url = fields.Str(required=False, missing=None)
    streams__start_time = fields.Int(required=False, missing=None)#don't know if it is correct
    streams__sport_id = fields.Int(required=False, missing=None)


class InputUserDTO(BaseDTO):
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class InputUserByEmailDTO(BaseDTO):
    email = fields.Str(required=True)


class NewPasswordDTO(BaseDTO):
    password = fields.Str(required=True)


class UpdateUserPreferencesDTO(BaseDTO):
    preferences = fields.List(fields.Int, required=True)
    user_id = fields.Int(required=True)
    type = fields.Str(required=True)


class GetUserPreferencesDTO(BaseDTO):
    user_id = fields.Int(required=False, missing=None)
    type = fields.Str(required=False, missing=None)


class InputUserByIdDTO(BaseDTO):
    user_id = fields.Int(required=False, missing=None)


class InputUserLogInDTO(BaseDTO):
    email = fields.Str(required=False, missing=None)
    email_or_username = fields.Str(required=False, missing=None)
    password = fields.Str(required=False, missing=None)
    auth_provider = fields.String(required=False, missing=None)


class TablesAndColumnsForUserPreferencesDTO:
    def __init__(self, main_table, related_table, user_id_field, type_id_field, related_name, related_logo, related_id):
        self.main_table = main_table
        self.related_table = related_table
        self.user_id_field = user_id_field
        self.type_id_field = type_id_field
        self.related_name = related_name
        self.related_logo = related_logo
        self.related_id = related_id
