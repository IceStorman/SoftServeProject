import os
import base64
from typing import Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText

from database.models import TempSubscribersData
from database.postgres.dal.user_subscription import UserSubscriptionDAL
from database.session import SessionLocal

from pathlib import Path

from dotenv import load_dotenv

from sqlalchemy import event

class UserSubscriptionManagerMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            _instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = _instance
        return cls._instances[cls]

class UserSubscriptionManager(metaclass=UserSubscriptionManagerMeta):
    __SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

    def __init__(self):
        self.__session = SessionLocal()

        current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
        envars = current_dir / ".env"
        load_dotenv(envars)

        self.__user_subscription_dal = UserSubscriptionDAL(self.__session)

        self.__sender_email = os.getenv("EMAIL")
        self.__sender_password = os.getenv("PASSWORD")

        event.listen(TempSubscribersData, "after_insert", self.__on_subscribers_inserted)

    def add_subscribers_to_temp_table(self, team_index):
        self.__user_subscription_dal.add_subscribers_data(team_index)

    def __on_subscribers_inserted(self, mapper, connection, target):
        self.__try_send_email_to_users()

    def __try_send_email_to_users(self):
        subscribed_users = self.__user_subscription_dal.get_subscribed_users_data_and_delete_rows()

        email_subject = "News notification"
        email_body = "The news with the team that you subscribed in have just been released"

        for user in subscribed_users:
            self.__send_email_to_user(user.subscriber_emails, email_subject, email_body)

    def __send_email_to_user(self, user_email: str, subject, body):
        creds = self.__authenticate_gmail()
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

    def __authenticate_gmail(self):
        creds = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.__SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                credentials_path = r"C:\Users\LEGION\Documents\Softserve\SoftServeProject\credentials.json"
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, self.__SCOPES)
                creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds

manager = UserSubscriptionManager()
manager.add_subscribers_to_temp_table(1)