from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    
    match_name = "Kings vs Pacers watch"

    
    base_url = "https://www.google.com/search"
    search_url = f"{base_url}?q={match_name.replace(' ', '+')}"

    
    driver.get(search_url)

    
    time.sleep(5)

    driver.find_elemens(By)
finally:
 
    driver.quit()
