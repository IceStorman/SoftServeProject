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

    def try_add_subscribers_to_temp_table(self, team_index, news_name):
        self.__user_subscription_dal.try_add_subscribers_data(team_index, news_name)

    def __on_subscribers_inserted(self, mapper, connection, target):
        self.__try_send_email_to_users()

    def __try_send_email_to_users(self):
        subscribed_users_email_data = self.__user_subscription_dal.pop_subscribed_users_data()

        for data in subscribed_users_email_data:
            self.__send_email_to_user(data.subscriber_emails, data.username, data.news_name, "-")

    def __send_email_to_user(self, user_email: str, username: str, news_name: str, team_name: str):
        from api.routes.__init__ import app
        with app.app_context():
            msg = Message(
                "News notification",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[user_email],
                html=self.__get_email_template(news_name, username, team_name)
            )
            current_app.extensions['mail'].send(msg)

            return CommonResponse().to_dict()

    def __get_email_template(self, news_name, username, team_name):
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("news_notification_email.html")
        main_part_of_url = current_app.config['FRONTEND_NEWS_URL']
        news_url = main_part_of_url + news_name

        return template.render(username=username, news_url=news_url, team_name=team_name)