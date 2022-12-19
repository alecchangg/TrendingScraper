from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

BASE = "http://127.0.0.1:5000/"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.youtube.com/")
driver.maximize_window()

trending = driver.find_element("link text", "Trending")
trending.click()

try:
    trendingImage =  WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse[2]/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/div[2]/div/div[1]/yt-img-shadow/img"))
    )
except:
    print("TREDNING ERROR")

all_videos = driver.find_elements("tag name", "ytd-video-renderer")
all_videos = all_videos[:48]

#video_rows = []

for video in all_videos:

    row = {}

    video_title = video.find_element("tag name", "h3")
    row["name"] = video_title.text

    channel_title_wrapper = video.find_element("tag name", "ytd-channel-name")
    channel_title = channel_title_wrapper.find_element("id", "text-container")
    row["channel"] = channel_title.text
    
    video_views_wrapper = video.find_element("css selector", '.text-wrapper.ytd-video-renderer')
    views_wrapper = video_views_wrapper.find_element("id", "metadata-line")
    video_views = views_wrapper.find_element("tag name", "span")
    row["views"] = video_views.text

    video_title.click()
    try:
        metadata = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "ytd-watch-metadata"))
        )
    except:
        print("NEXT ERROR")
    
    time.sleep(1)
    
    topRow = metadata.find_element("id", "top-row")   
    video_likes = topRow.find_element("xpath", '//*[@id="segmented-like-button"]/ytd-toggle-button-renderer/yt-button-shape/button/div[2]/span')
    row["likes"] = video_likes.text

    owner = topRow.find_element("id", "owner")
    channel_subs = owner.find_element("id", "owner-sub-count")
    row["subscribers"] = channel_subs.text
    

    response = requests.put(BASE + "video/", row)
    print(response)

    driver.back()

    try:
        trendingImage =  WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse[2]/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/div[2]/div/div[1]/yt-img-shadow/img"))
        )
    except:
        print("BACK PAGE ERROR!")
    time.sleep(0.5)


    
    #video_rows.append(row)


    

""" for row in range(len(video_rows)):
    response = requests.put(BASE + "video/", video_rows[row])
    print(response) """



driver.quit()


