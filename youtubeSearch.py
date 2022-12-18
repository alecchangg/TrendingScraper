from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


driver.get("https://www.youtube.com/")
driver.maximize_window()


search = driver.find_element("name", "search_query")
search.send_keys("comcast")
search.send_keys(Keys.RETURN)

try:
    c = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".yt-spec-touch-feedback-shape.yt-spec-touch-feedback-shape--touch-response"))
    )
    print("")
    print("Page loaded!")
    print("")

    time.sleep(3)

   
    content = driver.find_element('xpath', '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div[2]/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]')
    
    
    
    videos = content.find_elements("tag name", "ytd-video-renderer")
    
    for video in videos:
        video_title = video.find_element("tag name", "yt-formatted-string")
        print(video_title.text)
        #print("hello")
        print()
        print()
    
    time.sleep(5)
except:
    driver.quit()

driver.quit()