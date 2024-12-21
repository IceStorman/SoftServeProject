from typing import Dict
from database.models import TeamIndex
from database.postgres.postgres_country import save_country

def save_team(team_data: Dict, session, sport_id):
    if not team_data:
        return None

    if "team" in team_data:
        team_data = team_data.get("team")

    team_api_id = team_data.get('id')
    team_name = team_data.get('name')
    team_logo = team_data.get('logo')
    team_country_data = team_data.get('country', {})

    if not team_api_id or not team_name:
        return None

    country_entry = save_country(team_country_data, session)

    team_entry = session.query(TeamIndex).filter_by(api_id=team_api_id, sport_id=sport_id).first()
    if not team_entry:
        team_entry = TeamIndex(
            api_id=team_api_id,
            name=team_name,
            logo=team_logo,
            sport_id=sport_id,
            country=country_entry.country_id if country_entry else None
        )
        session.add(team_entry)
        session.commit()
    return team_entry

def save_teams(json_data: Dict, sport_id, session) -> None:
    teams = json_data.get("response", [])
    if not teams:
        print('insufficient data')
        return
    for team in teams:
        save_team(team, session, sport_id)