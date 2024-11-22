# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# import time
# import requests
# import shutil

# options = Options()
# arguments = [
#             "--headless", "--no-sandbox", "--disable-dev-shm-usage", "--disable-extensions"
#         ]
# for arg in arguments:
#     options.add_argument(arg)

# service = Service(ChromeDriverManager().install())
# prefs = {"download.default_directory" : "C:\\Users\\prots\\Downloads"};
# options.add_experimental_option("prefs",prefs)
# driver = webdriver.Chrome(service=service, options=options)


# try:
#     search_url = f"https://www.espn.com/nba/story/_/id/42509302/how-chris-paul-victor-wembanyama-evolving-together"
#     driver.get(search_url)
#     time.sleep(2)
#     counter = 0
#     image_elements = driver.find_elements(By.CSS_SELECTOR, ".imageLoaded")
#     for img in image_elements:
#         counter +=1
#         src = img.get_attribute('src')
#         url=src
#         print(url)

#         response = requests.get(url, stream=True)

#         with open(f'img{counter}.png', 'wb') as out_file:
#                shutil.copyfileobj(response.raw, out_file)
#         del response
        
        
        
# except Exception as e:
#     print(f"Error during image search: {e}")
# finally:
#     driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configure the WebDriver (replace with the path to your ChromeDriver)
options = Options()
arguments = [
            "--headless", "--no-sandbox", "--disable-dev-shm-usage", "--disable-extensions"
        ]
for arg in arguments:
    options.add_argument(arg)

service = Service(ChromeDriverManager().install())
prefs = {"download.default_directory" : "C:\\Users\\prots\\Downloads"};
options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(service=service, options=options)

# Open the target URL
driver.get("https://www.espn.com/nba/story/_/id/42509302/how-chris-paul-victor-wembanyama-evolving-together")

# Optionally scroll to load all lazy-loaded images
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for images to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Locate all image elements
images = driver.find_elements(By.CSS_SELECTOR, ".imageLoaded")

# Extract the `src` or `data-src` attributes
urls = []
for img in images:
    url = img.get_attribute("src") or img.get_attribute("data-src")
    if url:
        urls.append(url)

for url in urls:
    print("Lazy-loaded Image URL:", url)

# Close the browser
driver.quit()
