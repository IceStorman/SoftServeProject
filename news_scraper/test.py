# import unittest
# from unittest.mock import patch, MagicMock
# from bs4 import BeautifulSoup
# import requests
# from functionality import Main_page_sport_parser, Article_Scraper
# # from tokenizator import what_teams_here

# main_url = "https://www.espn.com/nba/" 
# parser = Article_Scraper(main_url)
# articles = parser.get_article_links(max_articles=3)  

# if articles:
#     for article in articles:
#         parser.print_article(article)  

        
#         content = parser.get_article_content(article['url'])
#         if content:
            
#             article_text = "\n".join(
#                 " ".join(section['content']) for section in content['article'].values()
#             )

            
#             # teams = what_teams_here(article_text)
#             # print("\nTeams mentioned in the article:")
#             # print(teams)
#         else:
#             print("Failed to fetch the content of the article.")
# else:
#     print("No articles found.")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

options = Options()
arguments = [
            "--no-sandbox", "--disable-dev-shm-usage", "--disable-extensions"
        ]
for arg in arguments:
        options.add_argument(arg)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

images = []

try:
    search_url = f"https://www.espn.com/nba/story/_/id/42509302/how-chris-paul-victor-wembanyama-evolving-together"
    driver.get(search_url)
    time.sleep(2)  
            
            
    image_elements = driver.find_elements(By.CSS_SELECTOR, ".imageLoaded.lazyloaded")
    for img in image_elements:
        src = img.get_attribute("src")
        if src:
            images.append(src)
            print(f"Found image: {src}")
except Exception as e:
        print(f"Error during image search: {e}")
finally:
        driver.quit()



