from marshmallow import Schema, fields
from flask_babel import _

class GameOutput(Schema):
    id = fields.Int()
    sport_id = fields.Int()
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
    sport_id = fields.Str()


class TeamsLeagueOutputWithCount(Schema):
    teams = fields.List(fields.Nested(TeamsLeagueOutput))
    count = fields.Int()


class PlayersOutput(Schema):
    name = fields.Str(attribute="name")
    id = fields.Str(attribute="api_id")
    logo = fields.Str(attribute="logo")


class StreamsOutput(Schema):
    id = fields.Str(attribute="stream_id")
    sport = fields.Int(attribute="sport_id")
    title = fields.Str()
    start_time = fields.DateTime()
    stream_url = fields.List(fields.Str())


class SportsOutput(Schema):
    id = fields.Int(attribute="sport_id")
    sport = fields.Str(attribute="sport_name")
    logo = fields.Str(attribute="sport_img")


class SportsLeagueOutput(Schema):
    id = fields.Int(attribute="api_id")
    sport = fields.Int(attribute="sport_id")
    logo = fields.Str()
    name = fields.Str()


class SportsLeagueOutputWithCount(Schema):
    teams = fields.List(fields.Nested(SportsLeagueOutput))
    count = fields.Int()


class CountriesOutput(Schema):
    id = fields.Int(attribute="country_id")
    flag = fields.Str()
    name = fields.Str()


class ListResponseDTO(Schema):
    items = fields.List(fields.Raw(), missing=[])
    count = fields.Int(missing=0)

    def __init__(self, items=None, count=None, **kwargs):
        super().__init__(**kwargs)
        self.items = items if items is not None else []
        self.count = count if count is not None else 0

    def to_dict(self):
        return {"items": self.items, "count": self.count}


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
    team_index_id = fields.Int(attribute="preferences")
    name = fields.Str(required=True)
    logo = fields.Str(required=True)


class OutputLogin():
    def __init__(self, email: str, user_id: int, token: str, username: str, new_user:bool, access_token:str, refresh_token:str):
        self.email = email
        self.user_id = user_id
        self.token = token
        self.username = username
        self.new_user = new_user
        self.access_token = access_token
        self.refresh_token = refresh_token
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
        "QSPORT":             _("QSPORT"),
        "since":              _("since 1990"),
        "sign_up_to":         _("Sign up to"),

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
        "required_field":     _("This field is required"),

        "confirm":            _("Confirm"),
        "skip":               _("Skip >"),
        "what_interesting_in": _("What are you interested in?"),
        "choose_sports":      _("Choose your favourite sports:"),

        "sign_up":            _("Sign Up"),
        "log_in":             _("Log In"),
        "password":           _("Password:"),
        "forget_password":    _("Forget password?"),
        "password_reset":     _("Password reset"),
        "no_account":         _("Do not have an account?"),
        "have_account":       _("Already have an account?"),
        "create":             _("Create"),
        "nickname":           _("Username:"),
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
        "search":             _("Search"),
        "all":                _("All"),
        "recommend_pref":     _("Recommended news by your Preferences"),
        "news_not_found":     _("No latest news were found"),
        "recommend_watch":    _("Recommended by your Last Watch"),
        "games_not_found":    _("Games not found"),
        "select_country":     _("Select a country..."),
        "apply_filters":      _("Apply Filters"),
        "search_name":        _("Search by name..."),
    }

