from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time


options = Options()
options.add_argument("start-maximized")
service = Service(".venv/chromedriver.exe")

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://dzen.ru/video")
time.sleep(5)

video_container = ".//a[contains(@class, 'video-site--card-video__cardLink-Ld')]"
# video_container = 'video-site--card-video__cardLink-Ld'
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, video_container))
)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

data = []
cards = driver.find_elements(By.XPATH, video_container)
count = 0

for card in cards:
    if count >= 10:
        break
    try:
        channel = card.find_element(
            By.XPATH, "//span[contains(@class, 'video-site--author-title__text-2Q')]"
        ).text
        name = card.find_element(
            By.XPATH,
            "//div[contains(@class, 'video-site--card-part-title__title-dF video-site--card-part-title__l-1t')]",
        ).text
        views = card.find_element(
            By.XPATH, "//div[contains(@class, 'video-site--meta__meta-3m')]/span[1]"
        ).text

        data.append({"channel": channel, "name": name, "views": views})
    except Exception as e:
        print(f"Ошибка при сборе данных: {e}")
    count += 1

with open("dzen_video_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

driver.quit()
