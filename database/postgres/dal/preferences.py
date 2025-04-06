from functools import lru_cache
from database.models import UserPreference, Sport, User, UserClubPreferences, TeamIndex
import database.models
from dto.api_input import TablesAndColumnsForUserPreferencesDTO
from service.api_logic.user_logic import PREFERENCES


class PreferencesDAL:

    def __init__(self, session=None):
        self.session = session


    def getattr_tables_and_columns_by_type(self, type_dto):
        main_table = getattr(database.models, type_dto.main_table, None)
        related_table = getattr(database.models, type_dto.related_table, None)
        user_id_field = getattr(main_table, type_dto.user_id_field, None)
        type_id_field = getattr(main_table, type_dto.type_id_field, None)
        related_name = getattr(related_table, type_dto.related_name, None)
        related_logo = getattr(related_table, type_dto.related_logo, None)
        related_id = getattr(related_table, type_dto.related_id, None)

        return TablesAndColumnsForUserPreferencesDTO(
            main_table=main_table,
            related_table=related_table,
            user_id_field=user_id_field,
            type_id_field=type_id_field,
            related_name=related_name,
            related_logo=related_logo,
            related_id=related_id
        )


    def get_user_preferences(self, type_dto, dto):
        tables_and_cols_dto = self.getattr_tables_and_columns_by_type(type_dto)

        user_prefs = (
            self.session.query(
                tables_and_cols_dto.user_id_field,
                TeamIndex.api_id,
                tables_and_cols_dto.type_id_field,
                tables_and_cols_dto.related_name,
                tables_and_cols_dto.related_logo
            )
            .join(tables_and_cols_dto.related_table, tables_and_cols_dto.type_id_field == tables_and_cols_dto.related_id)
            .filter(tables_and_cols_dto.user_id_field == dto.user_id)
        )
        return user_prefs.all()

    def delete_user_preferences(self, type_dto, dto, team_ids_by_api_id):
        tables_and_cols_dto = self.getattr_tables_and_columns_by_type(type_dto)

        team_index_ids = [t[0] for t in team_ids_by_api_id]

        if team_index_ids:
            self.session.query(tables_and_cols_dto.main_table).filter(
                tables_and_cols_dto.type_id_field.in_(team_index_ids),
                tables_and_cols_dto.user_id_field == dto.user_id
            ).delete(synchronize_session=False)

            self.session.commit()

    def delete_all_user_preferences(self, type_dto, dto):
        tables_and_cols_dto = self.getattr_tables_and_columns_by_type(type_dto)

        self.session.query(tables_and_cols_dto.main_table).filter(tables_and_cols_dto.user_id_field == dto.user_id).delete()
        self.session.commit()


    @lru_cache(maxsize=1)
    def get_all_sport_preference_indexes(self):
        return [
            sport.sport_id for sport in
            self.session.query(Sport.sport_id).order_by(Sport.sport_name.asc()).all()
        ]


    def get_existing_preferences(self, user_id, tables_and_cols_dto, type_dto):
        existing_api_ids = set(self.session.query(tables_and_cols_dto.type_id_field)
                   .filter(tables_and_cols_dto.user_id_field == user_id)
                   .all())

        if type_dto.type_id_field == PREFERENCES:
            existing_indices = set(self.session.query(TeamIndex.team_index_id)
                                    .filter(TeamIndex.api_id.in_([api_id[0] for api_id in existing_api_ids]))
                                    .all())

            return {idx[0] for idx in existing_indices}

        return {api_id[0] for api_id in existing_api_ids}


    def insert_new_preferences(self, new_prefs):
        self.session.add_all(new_prefs)
        self.session.commit()


    def delete_redundant_user_preferences(self, user_id, preferences_to_delete, tables_and_cols_dto):
        if not preferences_to_delete:
            return

        self.session.query(tables_and_cols_dto.main_table).filter(
            tables_and_cols_dto.user_id_field == user_id,
            tables_and_cols_dto.type_id_field.in_(preferences_to_delete)
        ).delete(synchronize_session=False)

        self.session.commit()

    def get_users_by_preference_index(self, preference_index):
        query = (
            self.session.query(User)
            .join(UserClubPreferences, User.user_id == UserClubPreferences.users_id)
            .filter(UserClubPreferences.preferences == preference_index)
            .all()
        )

        return query