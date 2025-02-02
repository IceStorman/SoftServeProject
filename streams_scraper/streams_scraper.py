from database.session import SessionLocal
from exept.exeptions import SportNotFoundError
from service.api_logic.streams_logic import save_json_stream_to_streams_table
from service.api_logic.sports_logic import get_sport_index_by_name
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from service.api_logic.games_logic import get_games_today


def configure_driver():

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True
    )
    return driver


def filter_future_games(games):
    
    return [
        f"{game['home_team_name']} vs {game['away_team_name']} {game['date']}"
        for game in games if game['status'] == 'Not Started'
    ]


def search_game_links(driver, future_games, games_today, session):
    
    base_url = "https://www.google.com/search"
    game_data = []

    for game in future_games:
        search_url = f"{base_url}?q={game.replace(' ', '+')}+watch"
        driver.get(search_url)
        links_elements = driver.find_elements(By.CLASS_NAME, 'LC20lb')
        urls = [link.get_attribute('href') for link in links_elements[:3]]

        matching_game = next(
            (g for g in games_today if f"{g['home_team_name']} vs {g['away_team_name']} {g['date']}" == game),
            None
        )
        start_time = matching_game['time'] if matching_game else "Unknown"

        sport_id = "unknown"
        if matching_game:
            sport_name = matching_game.get("sport_name", "unknown")
            try:
                sport_id = get_sport_index_by_name(session, sport_name)
            except SportNotFoundError:
                print(f"Sport '{sport_name}' not found in the database.")

        game_info = {
            "stream_url": urls[0] if urls else None,
            "start_time": start_time,
            "sport_id": sport_id
        }
        game_data.append(game_info)

    return game_data


def save_stream_data(session, game_data):
    
    streams_data = []

    for game in game_data:
        streams_data.append({
            "stream_url": game["stream_url"],
            "sport_id": game["sport_id"],
            "start_time": game["start_time"]
        })

    save_json_stream_to_streams_table(session, streams_data)


def main():
    
    session = SessionLocal()
    driver = configure_driver()

    try:
        
        
        games_today = get_games_today(session)
        future_games = filter_future_games(games_today)

        
        game_data = search_game_links(driver, future_games, games_today, session)

        
        save_stream_data(session, game_data)


    finally:
        driver.quit()
        session.close()


if __name__ == "__main__":
    main()
