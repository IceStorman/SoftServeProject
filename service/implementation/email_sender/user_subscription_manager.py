import os

from flask import current_app

from database.models import TempSubscribersData

from pathlib import Path
from dotenv import load_dotenv

from sqlalchemy import event

from jinja2 import Environment, FileSystemLoader
from flask_mail import Message

from dto.common_response import CommonResponse

class UserSubscriptionManager:
    def __init__(self, user_subscription_dal):
        self.__user_subscription_dal = user_subscription_dal

        current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
        envars = current_dir / ".env"
        load_dotenv(envars)

        event.listen(TempSubscribersData, "after_insert", self.__on_subscribers_inserted)

    def try_add_subscribers_to_temp_table(self, team_index):
        self.__user_subscription_dal.try_add_subscribers_data(team_index)

    def __on_subscribers_inserted(self, mapper, connection, target):
        self.__try_send_email_to_users()

    def __try_send_email_to_users(self):
        subscribed_users = self.__user_subscription_dal.get_subscribed_users_data_and_delete_rows()

        for user in subscribed_users:
            self.__send_email_to_user(user.subscriber_emails)

    def __send_email_to_user(self, user_email: str):
        from api.routes.__init__ import app
        with app.app_context():
            msg = Message(
                "News notification",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[user_email],
                html=self.__get_email_template()
            )
            current_app.extensions['mail'].send(msg)

            return CommonResponse().to_dict()

    def __get_email_template(self):
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("news_notification_email.html")

        return template.render()