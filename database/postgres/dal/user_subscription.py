from dask.array import delete
from sqlalchemy.orm import Session

from database.models import User, TempSubscribersData, UserClubPreferences


class UserSubscriptionDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_subscribers_data(self, preference_index):
        users = self.__get_users_by_preference_index(preference_index)

        new_rows = [
            TempSubscribersData(team_ids=preference_index, subscriber_emails=user.email)
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

    def get_subscribed_users_data_and_delete_rows(self):
        rows_to_delete = self.db_session.query(TempSubscribersData).all()

        subscribed_users = list()

        for row in rows_to_delete:
            copied_user = TempSubscribersData(team_ids=row.team_ids, subscriber_emails=row.subscriber_emails)
            subscribed_users.append(copied_user)

        self.db_session.query(TempSubscribersData).delete(synchronize_session=False)

        return subscribed_users