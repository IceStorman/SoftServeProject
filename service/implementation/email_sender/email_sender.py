from database.postgres.dal.club_preference import ClubPreferenceDAL
from database.postgres.dal.userEmail import UserEmailDAL
from database.session import SessionLocal

session = SessionLocal()

prefs_dal = ClubPreferenceDAL(session)
user_dal = UserEmailDAL(session)

def try_send_email_to_users(team_name: str):
    print("Trying to send email to users")
    subscribed_users = get_subscribed_users(team_name)

    for user in subscribed_users:
        user_email = get_user_email(user.user_id)
        send_email_to_user(user_email)

def get_subscribed_users(team_name: str):
    return prefs_dal.get_subscribed_users_on_specific_teams(team_name)

def get_user_email(user) -> str:
    return user_dal.get_user_email(user)

def send_email_to_user(user_email: str):
    print(user_email)

try_send_email_to_users("Caimanes")