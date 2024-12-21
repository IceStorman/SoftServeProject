from typing import Dict
from datetime import datetime
from database.models import Games
from database.postgres.postgres_country import extract_country, save_country
from database.postgres.postgres_team import save_team
from database.postgres.postgres_league import save_league

def save_games(json_data: Dict, sport_id, session) -> None:
    games = json_data.get("response", [])
    if not games:
        print('insufficient data')
        return

    for game in games:
        if "fixture" in game or "game" in game:
            separated_data = game.get("fixture") or game.get("game")
            api_id = separated_data.get("id")
            date = separated_data.get("date")
            status = separated_data.get('status')
        else:
            api_id = game.get('id')
            date = game.get('date')
            status = game.get('status')

        country_data = extract_country(game, "country")

        # (date) & time -----------
        if isinstance(date, dict):
            time = date.get('time')
            date = date.get('date')
        else:
            time = game.get('time')

        try:
            if isinstance(date, str):  # Якщо дата — рядок
                parsed_date = datetime.fromisoformat(date)  # Розбір ISO 8601 формату
            elif isinstance(date, datetime):  # Якщо це об'єкт datetime
                parsed_date = date
            else:
                raise ValueError("Невідомий формат дати")

            # Форматування дати
            date = parsed_date.strftime('%Y-%m-%d')
        except Exception as e:
            print(f"Помилка обробки дати для гри з ID {api_id}: {e}")
            date = None


            # status -----------------
        if not isinstance(status, str) and isinstance(status, dict):
            status = status.get('long')

        # league --------------------
        league_data = game.get('league')
        if isinstance(league_data, str):
            league_data = None # чи потрібно зберігати лігу, в якої відомо тільки назву?

        # teams ---------------------
        teams_data = game.get('teams', {})
        team_away_data = teams_data.get('away', {}) or teams_data.get('visitors', {})
        team_home_data = teams_data.get('home', {})

        # scores ---------------------------
        scores_data = game.get('scores', {}) or game.get('goals', {})
        score_away_data = scores_data.get('away') or scores_data.get('visitors')
        score_home_data = scores_data.get('home')
        if not isinstance(score_home_data, int) and isinstance(score_home_data, dict):
            score_home_data = score_home_data.get('points') or score_home_data.get('total')
        if not isinstance(score_away_data, int) and isinstance(score_away_data, dict):
            score_away_data = score_away_data.get('points') or score_away_data.get('total')

        league_entry = save_league(league_data, session, sport_id) if league_data else None
        country_entry = save_country(country_data, session) if country_data else None
        team_away_entry = save_team(team_away_data, session, sport_id)
        team_home_entry = save_team(team_home_data, session, sport_id)

        game_entry = session.query(Games).filter_by(api_id=api_id, sport_id=sport_id).first()
        if not game_entry:
            game_entry = Games(
                api_id=api_id,
                league_id=league_entry.league_id if league_entry else None,
                sport_id=sport_id,
                country_id=country_entry.country_id if country_entry else None,
                team_away_id=team_away_entry.team_index_id if team_away_entry else None,
                team_home_id=team_home_entry.team_index_id if team_home_entry else None,
                score_away_team=score_away_data,
                score_home_team=score_home_data,
                status=status,
                time=time,
                date=date
            )
            session.add(game_entry)
            session.commit()