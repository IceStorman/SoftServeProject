from marshmallow import Schema, fields
from flask_babel import _

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


def get_script_phrases():
    return {
        # Загальні
        "page_not_found":     _("Page not found"),
        "navigation":         _("Navigation"),
        "main_page":          _("Main page"),
        "about_us":           _("About us"),
        "faq":                _("FAQ"),
        "certatum_nostrum":   _("Certatum Nostrum"),
        "since":              _("since 1990"),

        # Контактна інформація
        "contact_info":       _("Contacts"),
        "address":            _("Address"),
        "phone":              _("Phone"),
        "email":              _("Email"),
        "our_social_media":   _("Socials"),

        # Авторизація
        "log_out":            _("Logout"),
        "account":            _("Account"),
        "change_preferences": _("Change preferences"),
        "delete_account":     _("Delete account"),
        "delete_check":       _("Are you sure?"),
        "delete_check_text":  _("Once deleted, the account cannot be restored"),
        "cancel":             _("Cancel"),

        "confirm":            _("Confirm"),
        "skip":               _("Skip >"),
        "what_interesting_in": _("What are you interested in?"),
        "choose_sports":      _("Choose your favourite sports:"),

        "sign_in":            _("Sign In"),
        "log_in":             _("Log In"),
        "password":           _("Password:"),
        "forget_password":    _("Forget password?"),
        "password_reset":     _("Password reset"),
        "no_account":         _("Do not have an account?"),
        "have_account":       _("Already have an account?"),
        "create":             _("Create"),
        "nickname":           _("Nickname:"),
        "repeat_password":    _("Repeat password:"),
        "email_account":      _("Email:"),

        # Новини та спорт
        "news":               _("News"),
        "leagues":            _("Leagues"),
        "filters":            _("Filters"),
        "games":              _("Games"),
        "latest_games":       _("Latest games"),
        "recommendations":    _("Recommendations"),
        "follow_teams":       _("to track performance of your favorite teams"),
        "tags":               _("Tags:"),
        "select_sport":       _("Select sport"),
        "teams":              _("teams"),

        # Додаткові опції
        "first_option":       _("Option 1"),
        "second_option":      _("Option 2"),
        "third_option":       _("Option 3"),
        "sort":               _("Sort by:"),
        "more":               _("more..."),
        "continue":           _("Continue?"),
    }

