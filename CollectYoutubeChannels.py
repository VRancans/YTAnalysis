from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

SCROLL_PAUSE_TIME = 2

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")

driver = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(driver, 10)

df = pd.DataFrame(columns = ['Name', 'Channel', 'Subscribers', 'Category'])

driver.get("https://socialblade.com/youtube/top/country/lv")
time.sleep(3)
wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='ACCEPT']"))).click()

for i in range(100):
    didNotGetToPage = True
    while didNotGetToPage:
        driver.get("https://socialblade.com/youtube/top/country/lv")
        time.sleep(3)

        youtuber_id = i + 5
        try:
            driver.find_element_by_xpath('/html/body/div[10]/div[2]/div[%s]/div[3]/a' % youtuber_id).click()
            time.sleep(2)
            didNotGetToPage = False
        except:
            didNotGetToPage = True

    v_youtuber = driver.find_element_by_xpath('//*[@id="YouTubeUserTopInfoBlockTop"]/div[1]/h1').text

    channel_child_elem = driver.find_element_by_xpath('//*[@id="YouTubeUserTopSocial"]/div/a/i[@class="fa fa-youtube-play"]')
    channel_elem = channel_child_elem.find_element_by_xpath("..")
    v_channel = channel_elem.get_attribute("href")
    v_channel += '/videos'

    v_subscribers = driver.find_element_by_xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[3]/span[2]').text

    v_category = ''
    try:
        v_category = driver.find_element_by_xpath('//*[@id="youtube-user-page-channeltype"]').text
    except:
        v_category = ''

    df.loc[len(df)] = [v_youtuber, v_channel, v_subscribers, v_category]

frames = [df]
df_copy = pd.concat(frames, axis=0, join='outer', join_axes=None, ignore_index=True,
                    keys=None, levels=None, names=None, verify_integrity=False, copy=True)
export_csv = df_copy.to_csv(r'lv-youtube-channels.csv', index=None, header=True, encoding='utf-8')
driver.close()