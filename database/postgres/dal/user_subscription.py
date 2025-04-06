from database.models import User, TempSubscribersData, UserClubPreferences, TeamIndex
from dto.api_output import TempSubscriberDataDto


class UserSubscriptionDAL:
    def __init__(self, session):
        self.db_session = session

    def try_add_subscribers_data(self, users, preference_index, news_name):
        new_rows = [
            TempSubscribersData(team_ids=preference_index, subscriber_emails=user.email, news_name=news_name)
            for user in users
        ]

        self.db_session.add_all(new_rows)
        self.db_session.commit()


    def pop_subscribed_users_data(self):
        rows_to_delete = (
            self.db_session.query(TempSubscribersData, User.username)
            .join(User, TempSubscribersData.subscriber_emails == User.email)
            .join(TeamIndex, TempSubscribersData.team_ids == TeamIndex.team_index_id)
            .all()
        )

        subscribed_users_data_for_email = [
            TempSubscriberDataDto(
                team_ids=row[0].team_ids,
                subscriber_emails=row[0].subscriber_emails,
                news_name=row[0].news_name,
                username=row[1]
            )
            for row in rows_to_delete
        ]
        self.db_session.query(TempSubscribersData).delete(synchronize_session=False)

        return subscribed_users_data_for_email