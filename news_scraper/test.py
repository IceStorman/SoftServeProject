from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import requests
from functionality import Main_page_sport_parser, Article_Scraper
import os


main_url = "https://www.espn.com/nba/" 
parser = Article_Scraper(main_url)
articles = parser.get_article_links(max_articles=3)  

if articles:
    for article in articles:
        parser.print_article(article)  

       
        content = parser.get_article_content(article['url'])
        if content:
           
            parser.write_article_into_json(article)
            
            
            article_text = "\n".join(
                " ".join(section['content']) for section in content['article'].values()
            )

            
            
        else:
            print("Failed to fetch the content of the article.")
else:
    print("No articles found.")




