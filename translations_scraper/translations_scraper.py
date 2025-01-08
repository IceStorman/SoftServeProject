from service.api_logic.games_logic import get_games_today
from database.session import SessionLocal
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from service.api_logic.streams_logic import save_json_stream_to_db
from service.api_logic.scripts import get_sport_index_by_name
from tempfile import TemporaryDirectory
import os




def configure_driver():
    options = Options()
    arguments = [
        "--headless", "--no-sandbox", "--disable-dev-shm-usage", "--disable-extensions"
    ]
    for arg in arguments:
        options.add_argument(arg)

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

def search_game_links(driver, future_games, games_today):
    base_url = "https://www.google.com/search"
    game_data = []

    with TemporaryDirectory() as temp_dir:
        for index, game in enumerate(future_games):
            search_url = f"{base_url}?q={game.replace(' ', '+')}+watch"
            links_elements = driver.find_elements(By.CLASS_NAME, 'LC20lb MBeuO DKV0Md')[:3]
            urls = [link.get_attribute('href') for link in links_elements]

            matching_game = next(
                (g for g in games_today if f"{g['home_team_name']} vs {g['away_team_name']} {g['date']}" == game),
                None
            )
            
            start_time = matching_game['time'] if matching_game else "Unknown"

            sport_id = "unknown"
            if matching_game:
                logo_url = matching_game.get("away_team_logo", "")
                if logo_url:
                    sport_id = logo_url.split(".io/")[1].split("/teams")[0]


            game_info = {
                "urls": urls,
                "start_time": start_time,
                "status": False,  
                "sport_id": sport_id
            }

            game_data.append(game_info)

            json_file_path = os.path.join(temp_dir, f"game_{index + 1}.json")
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(game_info, json_file, ensure_ascii=False, indent=4)

            print(f"Game data for '{game}' saved to: {json_file_path}")

    return game_data

def main():
    session = SessionLocal()
    driver = configure_driver()

    try:
        games = get_games_today(session)
        future_games = filter_future_games(games)
        
        search_game_links(driver, future_games)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
