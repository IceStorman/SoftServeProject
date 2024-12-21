from typing import Dict
from database.models import League
from database.postgres.postgres_country import save_country

def save_league(league_data, session, sport_id) -> League :
    if not league_data:
        return None

    league_api_id = league_data.get('id')
    league_name = league_data.get('name')
    league_logo = league_data.get('logo')
    league_country_data = league_data.get('country', {})

    if not league_name:
        return None

    country_entry = save_country(league_country_data, session)
    league_entry = session.query(League).filter_by(api_id=league_api_id, sport_id=sport_id).first()

    if not league_entry:
        league_entry = League(
            api_id=league_api_id,
            name=league_name,
            logo=league_logo,
            sport_id=sport_id,
            country=country_entry.country_id if country_entry else None
        )
        session.add(league_entry)
    else:
        league_entry.name = league_name
        league_entry.logo = league_logo
        league_entry.country = country_entry.country_id if country_entry else league_entry.country

    session.commit()
    return league_entry

def save_leagues(json_data: Dict, sport_id, session) -> None:
    leagues = json_data.get("response", [])
    if not leagues:
        print('Insufficient data')
        return

    for league in leagues:
        save_league(league, session, sport_id)
