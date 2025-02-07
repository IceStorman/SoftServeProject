from database.postgres.dal.club_preference import UserClubPreferenceDAL
from database.postgres.dal.userEmail import UserEmailDAL
from database.session import SessionLocal

session = SessionLocal()

prefs_dal = UserClubPreferenceDAL(session)
user_dal = UserEmailDAL(session)

class EmailSender:
    @staticmethod
    def try_send_email_to_users(team_index: int):
        subscribed_users = EmailSender.get_subscribed_users(team_index)

        for user_id in subscribed_users:
            user_email = EmailSender.get_user_email(user_id)
            EmailSender.send_email_to_user(user_email)

    @staticmethod
    def get_subscribed_users(team_index: int):
        return prefs_dal.get_subscribed_users_on_specific_teams(team_index)

    @staticmethod
    def get_user_email(user) -> str:
        return user_dal.get_user_email(user)

    @staticmethod
    def send_email_to_user(user_email: str):
        print(user_email)

EmailSender.try_send_email_to_users(1)