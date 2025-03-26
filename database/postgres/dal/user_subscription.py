from database.models import User, TempSubscribersData, UserClubPreferences, TeamIndex
from dto.api_output import TempSubscriberDataWithUsernameDto


class UserSubscriptionDAL:
    def __init__(self, session):
        self.db_session = session

    def try_add_subscribers_data(self, preference_index, news_name):
        users = self.__get_users_by_preference_index(preference_index)
        new_rows = [
            TempSubscribersData(team_ids=preference_index, subscriber_emails=user.email, news_name=news_name)
            for user in users
        ]

        self.db_session.add_all(new_rows)
        self.db_session.commit()

    def __get_users_by_preference_index(self, preference_index):
        query = (
            self.db_session.query(User)
            .join(UserClubPreferences, User.user_id == UserClubPreferences.users_id)
            .filter(UserClubPreferences.preferences == preference_index)
            .all()
        )

        return query

    def pop_subscribed_users_data(self):
        rows_to_delete = (
            self.db_session.query(TempSubscribersData, User)
            .join(User, TempSubscribersData.subscriber_emails == User.email)
            .join(TeamIndex, TempSubscribersData.team_ids == TeamIndex.team_index_id)
            .all()
        )

        subscribed_users_data_for_email = list()

        for row in rows_to_delete:
            copied_user = TempSubscriberDataWithUsernameDto(
                team_ids=row[0].team_ids,
                subscriber_emails=row[0].subscriber_emails,
                news_name=row[0].news_name,
                username=row[1].username
            )
            subscribed_users_data_for_email.append(copied_user)

        self.db_session.query(TempSubscribersData).delete(synchronize_session=False)

        return subscribed_users_data_for_email