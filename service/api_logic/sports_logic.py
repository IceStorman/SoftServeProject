from database.models import Sport
from exept.colors_text import print_error_message


def get_all_sports(session):
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


from database.models.league import League

def get_all_leagues_by_sport(session, sport_name, page, per_page):
    if sport_name is None or "Unknown":
        return {"error": "Not param sport_name"}
    offset = (page - 1) * per_page
    leagues = (
        session.query(League)
        .join(Sport, Sport.sport_id == League.sport_id)
        .filter(Sport.sport_name == sport_name)
        .limit(per_page)
        .offset(offset)
        .all()
    )
    if not leagues:
        print_error_message("No leagues found for the sport")
        return [], 204
    return [
        {
            "_id": league.league_id,
            "name": league.name,
            "logo": league.logo,
            "sport_name": sport_name
        }
        for league in leagues
    ], 200

