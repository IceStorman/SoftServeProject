import re
from collections import namedtuple
from datetime import datetime
from marshmallow import Schema, fields, pre_load, post_load, ValidationError


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

    @post_load
    def make_object(self, data, **kwargs):
        class_name = self.__class__.__name__.replace("Schema", "") or "DTO"
        return namedtuple(class_name, data.keys())(*data.values())

    @pre_load
    def validate_email(self, data, **kwargs):
        if 'email' in data and data['email']:
            if not re.match(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', data['email']):
                raise ValidationError("Invalid email format", field_name="email")
        return data

    @pre_load
    def validate_email(self, data, **kwargs):
        if 'username' in data and data['username']:
            regex = re.compile(r'[ @!#$%^&*()<>?/\|}{~:;,+=]')
            if regex.search(data['username']):
                raise ValidationError("Invalid username format", field_name="username")
        return data

    @pre_load
    def validate_password(self, data, **kwargs):
        if 'password_hash' in data and data['password_hash']:
            regex = re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?!.*\s){8,}')
            if not re.match(regex, data['password_hash']):
                raise ValidationError("Invalid password format", field_name="password_hash")
        return data


class TeamsLeagueDTO(BaseDTO):
    teams__sport_id = fields.Int(required=False, missing=None)
    leagues__api_id = fields.Int(required=False, missing=None)
    countries__api_id = fields.Int(required=False, missing=None)
    letter = fields.Str(required=False, missing="")
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
    password_hash = fields.Str(required=True)


class InputUserByEmailDTO(BaseDTO):
    email = fields.Str(required=True)


class NewPasswordDTO(BaseDTO):
    new_password = fields.Str(required=True)
    email = fields.Str(required=True)


class InputUserLoginDTO(BaseDTO):
    email_or_username = fields.Str(required=True)
    password_hash = fields.Str(required=True)


class UpdateUserPreferencesDTO(BaseDTO):
    preferences = fields.List(fields.Int, required=True)
    user_id = fields.Int(required=False, missing=None)


class GetUserPreferencesDTO(BaseDTO):
    user_id = fields.Int(required=False, missing=None)


class InputUserByGoogleDTO(BaseDTO):
    email = fields.Str(required=True)
    id = fields.Str(required=False, missing=None)
    verified_email = fields.Bool(required=False, missing=None)
    picture = fields.Str(required=False, missing=None)
    auth_url = fields.Str(required=False, missing=None)