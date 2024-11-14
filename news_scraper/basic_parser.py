from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import time

class Main_page_sport_parser:
    def __init__(self, main_url):
        self.main_url = main_url

    def get_article_links(self, max_articles=5):  
        response = requests.get(self.main_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = []
        for link in soup.find_all('a', class_="contentItem__padding contentItem__padding--border"):
            if len(articles) >= max_articles:  
                break

            article_url_suffix = link.get('href')
            title_tag = link.find('h2', class_='contentItem__title contentItem__title--story')
            if article_url_suffix and title_tag:
                title = title_tag.get_text()
                full_url = urljoin(self.main_url, article_url_suffix)
                articles.append({'title': title, 'url': full_url})
        
        return articles

class Article_Scraper(Main_page_sport_parser):
    def get_article_content(self, full_url):
        response = requests.get(full_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        timestamp = soup.select_one('.author .timestamp')
        
        article_data = {
            'timestamp': timestamp.get_text(strip=True) if timestamp else None,
            'sections': []
        }

        content_div = soup.select_one('.article-body')
        if content_div:
            elements = content_div.find_all(['p', 'h2'])

            current_section = None
            for element in elements:
                if element.name == 'h2':  
                    if current_section:
                        article_data['sections'].append(current_section)
                    current_section = {
                        'title': element.get_text(strip=True),
                        'content': []
                    }
                elif element.name == 'p':  
                    if current_section is None:
                        current_section = {'title': '', 'content': []}
                    current_section['content'].append(element.get_text(strip=True))

            if current_section:
                article_data['sections'].append(current_section)

        time.sleep(1)

        return article_data
    
    def print_article(self, article):
        print(f"Title: {article['title']}")
        print(f"URL: {article['url']}")
        content = self.get_article_content(article['url'])
        print(f"Timestamp: {content['timestamp']}\n")
        
        for section in content['sections']:
            if section['title']:
                print(f"Section: {section['title']}")
            for paragraph in section['content']:
                print(paragraph)
            print("\n")  
