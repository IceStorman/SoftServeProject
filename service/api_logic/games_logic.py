from sqlalchemy.testing import fixture

from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports

def get_games_today(session):
    blob_indexes = get_all_blob_indexes_from_db(session, "games.json") + \
                   get_all_blob_indexes_from_db(session, "fixtures.json")
    result = get_blob_data_for_all_sports(session, blob_indexes)
    return result

