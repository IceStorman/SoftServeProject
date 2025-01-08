from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By


article_data={
    'images':[]
}

options = Options()
arguments = [
            "--headless", "--no-sandbox", "--disable-dev-shm-usage", "--disable-extensions"
        ]
for arg in arguments:
    options.add_argument(arg)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
url='https://www.espn.com/nba/story/_/id/42933812/the-three-biggest-reasons-lebron-los-angeles-lakers-flailing-west'
driver.get(url)

driver.implicitly_wait(30)
image_sources = driver.execute_script(
    '''var els = document.getElementsByTagName('source');
    var imageSources = [];
    Array.from(els).forEach(img => {
        imageSources.push(img.getAttribute('data-srcset'));
    });
    return imageSources;'''
)
for i,image_source in enumerate(image_sources):
    if image_source is not None and(i==0 or i%2==0):
        sep =','
        images = image_source[:image_source.index(sep)]
        article_data['images'].append(images)
if not article_data['images']:
    try:
        search_url = f"https://www.google.com/search?tbm=isch&q={f'Warriors: Dennis Schroder to help Curry, Green in title chase'}"
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

for image in article_data['images']:
    print(image)

