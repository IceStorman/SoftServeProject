import random
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from api.container.container import Container
from dependency_injector.wiring import Provide, inject
from database.postgres.dto import StreamDTO
import re
from dto.api_input import GamesDTO, SearchDTO, PaginationDTO
from datetime import datetime
import undetected_chromedriver as uc

sport_dal = Provide[Container.sport_dal]

stream_service = Provide[Container.stream_service]
games_service = Provide[Container.games_service]


def configure_driver():
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features=AutomationControlled")

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    ]
    options.add_argument(f"user-agent={random.choice(user_agents)}")

    driver = uc.Chrome(options=options, use_subprocess=True)

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
        for game in games['items'] if game['status'] == 'Not Started'
    ]


def game_name(game):
    return f"{game['home_team_name']} vs {game['away_team_name']}"


def sport_name(url):
    match = re.search(r'api-sports.io/([^/]+)/teams', url)
    return match.group(1) if match else "unknown"


def search_game_links(driver, future_games, games_today):
    base_url = "https://www.bing.com/search"
    stream_data = []

    streams_number = 1
    for game in future_games:
        search_url = f"{base_url}?q={game.replace(' ', '+')}+watch"
        driver.get(search_url)
        links_elements = driver.find_elements(By.XPATH, '//h2/a')
        urls = [link.get_attribute('href') for link in links_elements[:3]]

        matching_game = next(
            (g for g in games_today['items'] if f"{g['home_team_name']} vs {g['away_team_name']} {g['date']}" == game),
            None
        )

        if not matching_game:
            continue

        print(f"Matched stream #{streams_number} is being processed")
        streams_number += 1

        date = datetime.strptime(matching_game.get("date"), "%Y-%m-%d")
        stream_dto = StreamDTO(
            title=game_name(matching_game),
            stream_urls=urls if urls else None,
            start_time=date,
            sport_id=matching_game.get("sport_id")
        )
        stream_data.append(stream_dto)

    return stream_data


@inject
def save_stream_data(streams_data):
    stream_service.save_streams_to_streams_table(streams_data)


@inject
def main():
    driver = configure_driver()

    try:
        dto = SearchDTO().load({
            "filters": [
                {
                 "filter_name": "date_from",
                 "filter_value": datetime.now().date()
                }
            ]
        })
        games_today = games_service.get_games_today(dto)

        if games_today["count"] <= 0:
            print("No available games for now.")
            return

        future_games = filter_future_games(games_today)
        game_data = search_game_links(driver, future_games, games_today)
        save_stream_data(game_data)

    finally:
        print("Links Parsing Is Finished")

        if driver:
            driver.quit()


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    main()
