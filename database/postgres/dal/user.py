from sqlalchemy import or_
from database.models import User, UserClubPreferences, UserPreference


class UserDAL:
    def __init__(self, session = None):
        self.session = session

    def get_user_by_email_or_username(self, email = None, username = None):
        filters = []

        if email:
            filters.append(User.email == email)

        if username:
            filters.append(User.username == username)

        if not filters:
            return None

        return self.session.query(User).filter(or_(*filters)).first()

    def create_user(self, new_user):
        self.session.add(new_user)
        self.session.commit()

    def get_user_by_id(self, user_id: int) -> User:
        return self.session.query(User).filter(User.user_id == user_id).first()

    def update_user_password(self, user: User, new_password):
        user.password_hash = new_password
        self.session.commit()

    def get_user_id_be_email(self, email: str) -> User:
        return self.session.query(User).filter(User.email == email).first()

    def get_all_users(self):
        return self.session.query(User).all()

    def get_user_sport_and_club_preferences_by_native_id(self, user_id):
        query = (
            self.session.query(
                UserClubPreferences.preferences,
                UserPreference.sports_id
            )
            .select_from(User)
            .join(UserClubPreferences, UserClubPreferences.users_id == User.user_id)
            .join(UserPreference, UserPreference.users_id == User.user_id)
            .filter(User.user_id == user_id)
        )

        return query.all()
