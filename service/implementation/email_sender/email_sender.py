from database.models import TeamIndex
from database.postgres.dal.club_preference import ClubPreferenceDAL
from database.postgres.dal.user import UserDAL
from database.session import SessionLocal

session = SessionLocal()

prefs_dal = ClubPreferenceDAL(session)
user_dal = UserDAL(session)

def try_send_email_to_users(team_index: TeamIndex):
    subscribed_users = get_subscribed_users(team_index)

    for user in subscribed_users:
        user_email = get_user_email(user)
        send_email_to_user(user_email)

def get_subscribed_users(team_index: TeamIndex):
    return prefs_dal.get_subscribed_users_on_specific_teams(team_index)

def get_user_email(user) -> str:
    return user_dal.get_user_email(user)

def send_email_to_user(user_email: str):
    print(user_email)