from database.session import SessionLocal
from database.models import Sport, TeamIndex
from typing import Dict
from database.postgres.postgres_league import save_leagues
from database.postgres.postgres_game import save_games

TEAMS = 'teams'
LEAGUES = 'leagues'
GAMES = ["games", "fixtures", "fights", "races", "competitions"]

def save_api_data(json_data: Dict, sport_name: str ) -> None:
    session = SessionLocal()
    try:
        sport = session.query(Sport).filter_by(sport_name=sport_name).first()
        if sport:
            sport_id = sport.sport_id
        else:
            print(f"added new sport_id for {sport_name}.")
            sport_entry = Sport(sport_name)
            session.add(sport_entry)
            session.commit()
            sport_id = sport_entry.sport_id

        entity = json_data.get("get")
        json_data = json_data.get("response", [])

        if entity == TEAMS:
            for team in json_data:
                TeamIndex(team, sport_id).save()
                '''                save_teams(json_data, sport_id, session)
            if sport_name == "mma" or sport_name == "formula-1":
                save_leagues(json_data, sport_id, session)'''
        elif entity == LEAGUES:
            save_leagues(json_data, sport_id, session)

        elif entity in GAMES:
            save_games(json_data, sport_id, session)

    except Exception as e:
        session.rollback()
        print("data was screwed up")
        print(f"error processing data: {e}")