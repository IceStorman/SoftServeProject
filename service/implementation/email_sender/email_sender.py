import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText

from database.models import TempSubscribersData
from database.postgres.dal.club_preference import UserClubPreferenceDAL
from database.postgres.dal.user_email import UserEmailDAL
from database.session import SessionLocal

from pathlib import Path

from dotenv import load_dotenv

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

class SubscriptionManager:
    session = SessionLocal()

    __current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
    __envars = __current_dir / ".env"
    load_dotenv(__envars)

    __prefs_dal = UserClubPreferenceDAL(session)
    __user_dal = UserEmailDAL(session)

    __sender_email = os.getenv("EMAIL")
    __sender_password = os.getenv("PASSWORD")

    @staticmethod
    def add_subscribers_to_temp_table(team_index):
        users = SubscriptionManager.__user_dal.get_users_by_preference_index(team_index)

        new_rows = [
            TempSubscribersData(team_ids=team_index, subscriber_emails=user.email)
            for user in users
        ]

        SubscriptionManager.session.add_all(new_rows)
        SubscriptionManager.session.commit()

    @staticmethod
    def try_send_email_to_users(team_index: int):
        subscribed_users_emails = SubscriptionManager.__get_subscribed_users_emails(team_index)

        for user_id in subscribed_users_emails:
            user_email = SubscriptionManager.__get_user_email(user_id)
            SubscriptionManager.__send_email_to_user(user_email, "News notification", "The news with the team that you subscribed in have just been released")

    @staticmethod
    def __get_subscribed_users_emails(team_index):
        pass

    @staticmethod
    def __send_email_to_user(user_email: str, subject, body):
        creds = SubscriptionManager.__authenticate_gmail()
        service = build("gmail", "v1", credentials=creds)

        message = MIMEText(body)
        message["to"] = user_email
        message["subject"] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        send_message = service.users().messages().send(
            userId="me",
            body={"raw": raw_message}
        ).execute()

        print(f"Email sent successfully! Message ID: {send_message['id']}")

    @staticmethod
    def __authenticate_gmail():
        creds = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                credentials_path = r"C:\Users\LEGION\Documents\Softserve\SoftServeProject\credentials.json"
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds


SubscriptionManager.add_subscribers_to_temp_table(1)