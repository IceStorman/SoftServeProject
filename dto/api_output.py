from marshmallow import Schema, fields


class GameOutput(Schema):
    id = fields.Int(attribute="api_id")
    status = fields.Str()
    date = fields.Str()
    time = fields.Str()
    league_name = fields.Str()
    league_logo = fields.Str()
    country_name = fields.Str()
    home_team_name = fields.Str()
    home_team_logo = fields.Str()
    away_team_name = fields.Str()
    away_team_logo = fields.Str()
    home_score: fields.Int(attribute="score_home_team")
    away_score: fields.Int(attribute="score_away_team")


class TeamsLeagueOutput(Schema):
    league_name = fields.Str(attribute="league")
    country_name = fields.Str(attribute="country")
    team_name = fields.Str(attribute="name")
    logo = fields.Str()
    id = fields.Str(attribute="api_id")


class SportsOutput(Schema):
    id = fields.Int(attribute="sport_id")
    sport = fields.Str(attribute="sport_name")
    logo = fields.Str(attribute="sport_img")


class SportsLeagueOutput(Schema):
    id = fields.Int(attribute="league_id")
    sport = fields.Int(attribute="sport_id")
    logo = fields.Str()
    name = fields.Str()

class CountriesOutput(Schema):
    id = fields.Int(attribute="api_id")
    flag = fields.Str()
    name = fields.Str()