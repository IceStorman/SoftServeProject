from database.models import Sport
from exept.colors_text import print_error_message
#from database.models.league import League

def get_all_sports(session):
    try:
        sports = session.query(Sport).all()
        if not sports:
            print_error_message("No sports found in the database")
            return [], 204
        return [
            {
                "sport_id": sport.sport_id,
                "sport_name": sport.sport_name,
                "sport_img": sport.sport_img
            } for sport in sports], 200
    except Exception as e:
        raise Exception

'''
def get_all_leagues_by_sport(session, name):
    try:
        leagues = session.query(League).filter(League.name == name).all()
        if not leagues:
            print_error_message("No leagues found in the database")
            return [], 204
        return [
            {
                "_id": league.league_id,
                "name": league.name,
                "logo": league.logo
            } for league in leagues], 200
    except Exception as e:
        raise Exception
'''