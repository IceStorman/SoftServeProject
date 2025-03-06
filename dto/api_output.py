from marshmallow import Schema, fields

class GameOutput(Schema):
    id = fields.Int()
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
    home_score = fields.Int(attribute="score_home_team")
    away_score = fields.Int(attribute="score_away_team")


class TeamsLeagueOutput(Schema):
    league_name = fields.Str(attribute="league")
    team_name = fields.Str(attribute="name")
    logo = fields.Str()
    id = fields.Str(attribute="api_id")
    count = fields.Int()

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
    id = fields.Int(attribute="country_id")
    flag = fields.Str()
    name = fields.Str()

class OutputUser(Schema):
    username = fields.Str(required=True)
    email = fields.Str(required=True)

class OutputSportPreferences(Schema):
    user_id = fields.Int(required=True)
    sports_id = fields.Str(required=True)
    sport_name = fields.Str(required=True)
    sport_img = fields.Str(required=True)

class OutputTeamPreferences(Schema):
    user_id = fields.Int(required=True)
    team_index_id = fields.Str(required=True)
    name = fields.Str(required=True)
    logo = fields.Str(required=True)

class OutputLogin():
    def __init__(self, email: str, id: int, token: str):
        self.email = email
        self.id = id
        self.token = token
        self.message = "You successfully logged in!"


class OutputRecommendationList(Schema):
    news_id = fields.Int(required=True)
    score = fields.Float(required=True)
    user_id = fields.Int(required=True)
    rating = fields.Int(required=True)

