from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
from tokenizator import what_teams_here
from database.azure_blob_storage.save_get_blob import blob_save_news



class Main_page_sport_parser:
    def __init__(self, main_url):
        self.main_url = main_url
        self.articles = []

    def get_article_links(self, max_articles=5):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(self.main_url, headers=headers)

        if response.status_code != 200:
            print(f"Error fetching the page. Status code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        articles = []
        for first_div in soup.find_all('div', class_='interior secondary'):
            first_section = first_div.find('section', {'id': 'pane-main'})
            if first_section:
                secondary_section = first_section.find('section', {'id': 'main-container'})
                if secondary_section:
                    second_div = secondary_section.find('div', class_='main-content layout-dbc one-feed')
                    if second_div:
                        third_section = second_div.find('section', {'id': 'news-feed'})
                        if third_section:
                            fourth_sections = third_section.find_all('section', class_='contentItem contentItem--collection')
                            for fourth_section in fourth_sections:
                                fifth_section = fourth_section.find('section', class_='contentItem__content contentItem__content--story has-image has-video contentItem__content--collection contentItem__content--enhanced contentItem__content--fullWidth')
                                if fifth_section:
                                    a_tag = fifth_section.find('a', class_='contentItem__padding contentItem__padding--border')
                                    if a_tag:
                                        article_url_suffix = a_tag.get('href')
                                        third_div = a_tag.find('div', class_='contentItem__contentWrapper')
                                        if third_div:
                                            fourth_div = third_div.find('div', class_='contentItem__titleWrapper')
                                            if fourth_div:
                                                title_tag = fourth_div.find('h2', class_='contentItem__title contentItem__title--story')

                                                if article_url_suffix and title_tag:
                                                    title = title_tag.get_text()
                                                    full_url = urljoin(self.main_url, article_url_suffix)
                                                    articles.append({'title': title, 'url': full_url})
                                if len(articles) >= max_articles:
                                    break

        print(f"Found {len(articles)} articles:")
        for article in articles:
            print(f"Title: {article['title']}, URL: {article['url']}")

        self.articles=articles
        return articles

class Article_Scraper(Main_page_sport_parser):
        

    def get_article_content(self, full_url):
        options = Options()
        arguments = [
            "--headless", "--no-sandbox", "--disable-dev-shm-usage", "--disable-extensions"
        ]
        for arg in arguments:
            options.add_argument(arg)

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(full_url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching the article. Status code: {response.status_code}")
            driver.quit()
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        article_data = {
            'title': None,
            'timestamp': None,
            'article': {},
            'images': [],
            'team_names': [],
            'S_P_O_R_T': None
        }

        
        sport_urls = {
            'main_formula-1_url': 'https://www.espn.com/f1/',
            'main_football_url': 'https://www.espn.com/soccer/',
            'main_afl_url': '',
            'main_baseball_url': 'https://www.espn.com/mlb/',
            'main_basketball_url': '',
            
            'main_handball_url': '',
            'main_hockey_url': 'https://www.espn.com/nhl/',
            'main_mma_url': 'https://www.espn.com/mma/',
            'main_nba_url': 'https://www.espn.com/nba/',
            'main_nfl_url': 'https://www.espn.com/nfl/',
            'main_rugby_url': 'https://www.espn.com/rugby/',
            'main_volleyball_url': ''
        }

        
        for sport_key, sport_url in sport_urls.items():
            if sport_url and sport_url in full_url:
            
                article_data['S_P_O_R_T'] = sport_key.replace('main_', '').replace('_url', '').replace('_', ' ').capitalize()
                break

        title = soup.title.string if soup.title else "Unknown Article"
        article_data['title'] = title

        try:
            search_url = f"https://www.google.com/search?tbm=isch&q={title}"
            driver.get(search_url)
            time.sleep(2)
            image_elements = driver.find_elements(By.CLASS_NAME, "YQ4gaf")[:3]
            for img in image_elements:
                src = img.get_attribute("src")
                if src:
                    article_data['images'].append(src)
                    print(f"Found image: {src}")
        except Exception as e:
            print(f"Error during image search: {e}")
        finally:
            driver.quit()

        timestamp = soup.select_one('.author .timestamp')
        article_data['timestamp'] = timestamp.get_text(strip=True) if timestamp else time.strftime("%Y-%m-%d")

        for aside in soup.find_all('aside', class_=['inline editorial float-r', 'inline float-r inline-track']):
            aside.decompose()

        content_div = soup.select_one('.article-body')
        if content_div:
            elements = content_div.find_all(['p', 'h2', 'h3'])
            current_section_title = None
            current_section_content = []
            current_section_subheadings = []
            section_counter = 1

            for element in elements:
                if element.name == 'h2':  
                    if current_section_title or current_section_content:
                        article_data['article'][f'section_{section_counter}'] = {
                            'heading': current_section_title,
                            'subheadings': current_section_subheadings,
                            'content': current_section_content,
                        }
                        section_counter += 1

                    current_section_title = element.get_text(strip=True)
                    current_section_content = []
                    current_section_subheadings = []

                elif element.name == 'h3':  
                    current_section_subheadings.append(element.get_text(strip=True))

                elif element.name == 'p':  
                    current_section_content.append(element.get_text(strip=True))

            if current_section_title or current_section_content:
                article_data['article'][f'section_{section_counter}'] = {
                    'heading': current_section_title,
                    'content': current_section_content,
                    'subheadings': current_section_subheadings
                }
            teams = what_teams_here(json.dumps(article_data['article']))
            article_data['team_names'].append(teams)

        time.sleep(1)
        return article_data



    def print_article(self, article):
        print(f"\n---\nTitle: {article['title']}")
        print(f"URL: {article['url']}")
        
        content = self.get_article_content(article['url'])

        if not content:
            print("Failed to fetch the content of the article.")
            return


        sport_type = content.get('S_P_O_R_T', 'Unknown Sport')
        print(f"Sport Type: {sport_type}")
        print(f"Timestamp: {content['timestamp']}\n")

        if content['images']:
            print("Images found:")
            for idx, img_url in enumerate(content['images'], start=1):
                print(f"{idx}. {img_url}")
        else:
            print("No images found.")

        for section_key, section_data in content['article'].items():
            title = section_data['heading']
            paragraphs = section_data['content']
            subheadings = section_data.get('subheadings', [])

            print(f"\nSection Title: {title}\n")

            for idx, paragraph in enumerate(paragraphs):
                if idx < len(subheadings) and subheadings[idx]:
                    print(f"Subheading: {subheadings[idx]}\n")

                formatted_paragraph = paragraph.replace('<br>', '\n\t')
                print(f"Paragraph Text:\n\t{formatted_paragraph}\n")

        print("End of Article\n---")

    def write_article_into_json(self, article):
        content = self.get_article_content(article['url'])
        if not content:
            print(f"Failed to fetch content for: {article['title']}")
            return

        invalid_chars = r'<>:"/\|?*'
        sanitized_title = ''.join(c if c not in invalid_chars else '_' for c in article['title'])
        filename = sanitized_title.replace(" ", "_") + ".json"
        filepath = os.path.join("articles", filename)

        os.makedirs("articles", exist_ok=True)

        try:

            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(content, file, ensure_ascii=False, indent=4)
            print(f"Article saved locally: {filepath}")

            blob_save_news(content)
            print(f"Article uploaded to Azure Blob Storage successfully.")

        except Exception as e:
            print(f"Error saving article '{filename}': {e}") 
