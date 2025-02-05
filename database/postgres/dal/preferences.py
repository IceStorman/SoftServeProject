from database.models import UserPreference, Sport
import database.models
from dto.api_input import TablesAndColumnsDTO
from service.api_logic.sports_logic import get_all_sports


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

        return TablesAndColumnsDTO(
            main_table=main_table,
            related_table=related_table,
            user_id_field=user_id_field,
            type_id_field=type_id_field,
            related_name=related_name,
            related_logo=related_logo,
            related_id=related_id
        )


    def get_all_sport_preferences(self):
        return get_all_sports()


    def add_user_preferences(self, type_dto, dto, valid_preferences):
        tables_and_cols_dto = self.getattr_tables_and_columns_by_type(type_dto)

        for pref in valid_preferences:
            exists = self.session.query(tables_and_cols_dto.main_table).filter(tables_and_cols_dto.user_id_field == dto.user_id, tables_and_cols_dto.type_id_field == pref).first()
            if not exists:
                new_pref = tables_and_cols_dto.main_table(**{
                    type_dto.user_id_field: dto.user_id,
                    type_dto.type_id_field: pref
                })
                self.session.add(new_pref)
        self.session.commit()


    def get_user_preferences(self, type_dto, dto):
        tables_and_cols_dto = self.getattr_tables_and_columns_by_type(type_dto)

        user_prefs = (
            self.session.query(
                tables_and_cols_dto.user_id_field,
                tables_and_cols_dto.type_id_field,
                tables_and_cols_dto.related_name,
                tables_and_cols_dto.related_logo
            )
            .join(tables_and_cols_dto.related_table, tables_and_cols_dto.type_id_field == tables_and_cols_dto.related_id)
            .filter(tables_and_cols_dto.user_id_field == dto.user_id)
            .all()
        )
        return user_prefs


    def delete_user_preferences(self, type_dto, dto):
        tables_and_cols_dto = self.getattr_tables_and_columns_by_type(type_dto)

        for pref in dto.preferences:
            self.session.query(tables_and_cols_dto.main_table).filter(tables_and_cols_dto.type_id_field == pref, tables_and_cols_dto.user_id_field == dto.user_id).delete()
        self.session.commit()


    def delete_all_user_preferences(self, type_dto, dto):
        tables_and_cols_dto = self.getattr_tables_and_columns_by_type(type_dto)

        self.session.query(tables_and_cols_dto.main_table).filter(tables_and_cols_dto.user_id_field == dto.user_id).delete()
        self.session.commit()


    def get_all_sport_preference_indexes(self):
        return [
            sport.sport_id for sport in
            self.session.query(Sport.sport_id).order_by(Sport.sport_name.asc()).all()
        ]
