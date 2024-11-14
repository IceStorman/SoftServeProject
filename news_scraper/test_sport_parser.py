import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import requests
from basic_parser import Main_page_sport_parser, Article_Scraper



main_url = "https://www.espn.com/nba/" 
parser = Article_Scraper(main_url)
articles = parser.get_article_links(max_articles=2)  

if articles:
    for article in articles:
        parser.print_article(article)
else:
    print("No articles found.")


