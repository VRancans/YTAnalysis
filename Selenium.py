from selenium import webdriver 
import pandas as pd 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import emoji
import regex
import re

def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(r'', text)
    
def split_count(text):
    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)

    return emoji_list

SCROLL_PAUSE_TIME = 2

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")

driver = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(driver, 20)

# define columns for the csv file that we are going to make
df = pd.DataFrame(columns = ['youtuber', 'video_link', 'title', 'views', 'upload_date', 'likes', 'dislikes', 'comment', 'word_count', 'emoji_count', 'average_word_length'])
try:
    with open('filtered-lv-youtube-channels.csv', mode='r', encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
                youtuber = row["Name"]
                channel = row["Channel"]

                driver.get(channel)
                time.sleep(1.5)

                try:
                    driver.find_element_by_xpath("//span[text()='Uploads']").click()
                    time.sleep(1.5)
                except:
                    print("No 'Uploads' section found")

                last_height = driver.execute_script("return document.documentElement.scrollHeight")
                i = 0
                while False:    #i is the amount of scrolls performed. Youtube loads 30 videos every scroll, so (i+1) * 30 would be the max amount of videos found in channel, do to 30 videos being loaded initially. Replace "i < x" with "True" if you want to read all videos, set to "False" if you only want the first 30.
                    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
                    time.sleep(SCROLL_PAUSE_TIME)

                    new_height = driver.execute_script("return document.documentElement.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                    i = i + 1

                # after scrolling through videos page, let's get all the video links
                user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
                links = []
                for i in user_data:
                    links.append(i.get_attribute('href'))

                print(len(links))

                # if you want to use a specific amount of videos from "links" variable, do links = links[:x] which means first x videos

                v_youtuber = youtuber

                for x in links:
                    driver.get(x)
                    time.sleep(1.5)

                    v_video_link = x

                    v_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text

                    v_views = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="count"]/yt-view-count-renderer/span[1]'))).text
                    v_views = v_views.replace(" views", "")
                    v_views = v_views.replace(",", "")

                    v_upload_date = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="date"]/yt-formatted-string'))).text

                    v_likes = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[1]/a/yt-formatted-string'))).text
                    v_likes = v_likes.replace("K", "000")
                    v_likes = v_likes.replace("M", "000000")
                    if "." in v_likes:
                        v_likes = v_likes.replace(".", "")
                        v_likes = int(v_likes) / 10


                    v_dislikes = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[2]/a/yt-formatted-string'))).text
                    v_dislikes = v_dislikes.replace("K", "000")
                    v_dislikes = v_dislikes.replace("M", "000000")
                    if "." in v_dislikes:
                        v_dislikes = v_dislikes.replace(".", "")
                        v_dislikes = int(v_dislikes) / 10

                    last_height = driver.execute_script("return document.documentElement.scrollHeight")
                    i = 0 #max readable comments = i*20
                    while i < 4:
                        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")

                        time.sleep(SCROLL_PAUSE_TIME)

                        new_height = driver.execute_script("return document.documentElement.scrollHeight")
                        if new_height == last_height:
                            break
                        last_height = new_height
                        i = i + 1

                    comment_elements = driver.find_elements_by_css_selector("ytd-comment-renderer#comment div#body div#main ytd-expander#expander div#content yt-formatted-string#content-text")
                    for element in comment_elements:
                        v_comment = element.text

                        ############################### processing of comment ################################

                        emojiless_comment = remove_emoji(v_comment)
                        v_word_count = len(re.findall(r'\w+', emojiless_comment))

                        emojis_in_comment = split_count(v_comment)
                        v_emoji_count = len(emojis_in_comment)

                        if v_word_count == 0:
                            v_average_word_length = 0
                        else:
                            words = re.findall(r'\w+', emojiless_comment)
                            v_average_word_length = sum(len(word) for word in words) / v_word_count
                        ######################################################################################
                        df.loc[len(df)] = [v_youtuber, v_video_link, v_title, v_views, v_upload_date, v_likes, v_dislikes, v_comment, v_word_count, v_emoji_count, v_average_word_length]
except:
    print("something failed when trying to get data")

frames = [df]
df_copy = pd.concat(frames, axis=0, join='outer', join_axes=None, ignore_index=True,
                        keys=None, levels=None, names=None, verify_integrity=False, copy=True)

export_csv = df_copy.to_csv (r'lv-youtuber-comments-v5.csv', index = None, header=True, encoding='utf-8')
driver.close()