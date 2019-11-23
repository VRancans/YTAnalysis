from selenium import webdriver 
import pandas as pd 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import emoji
import regex

def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(u'', text)
    
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
wait = WebDriverWait(driver, 10)

with open('youtube-channels.csv', mode='r', encoding="utf8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
            youtuber = row["Name"]
            channel = row["Channel"]
            
            driver.get(channel)
            time.sleep(1.5)

            last_height = driver.execute_script("return document.documentElement.scrollHeight")
            i = 0
            while False:    #i is the amount of scrolls performed. Youtube loads 30 videos every scroll, so (i+1) * 30 would be the max amount of videos found in channel, do to 30 videos being loaded initially. Replace "i < x" with "True" if you want to read all videos
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

            # if you want to use a specific amount of videos, do links = links[:x] which means first x videos

            links = links[:15]
            # define columns for the csv file we are going to make
            
            df = pd.DataFrame(columns = ['youtuber', 'video_link', 'title', 'comment', 'word_count', 'emoji_count', 'average_word_length'])

            v_youtuber = youtuber

            for x in links:
                driver.get(x)
                time.sleep(1.5)
                v_video_link = x
                v_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
                
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
                    v_word_count = len(emojiless_comment.split())
                    
                    emojis_in_comment = split_count(v_comment)
                    v_emoji_count = len(emojis_in_comment)
                    
                    if v_word_count == 0:
                        v_average_word_length = 0
                    else:
                        words = emojiless_comment.split()
                        v_average_word_length = sum(len(word) for word in words) / v_word_count
                    ######################################################################################
                    df.loc[len(df)] = [v_youtuber, v_video_link, v_title, v_comment, v_word_count, v_emoji_count, v_average_word_length]

            frames = [df]
            df_copy = pd.concat(frames, axis=0, join='outer', join_axes=None, ignore_index=True,
                                        keys=None, levels=None, names=None, verify_integrity=False, copy=True)
                                        
            export_csv = df_copy.to_csv (r'comments-%s.csv' % youtuber, index = None, header=True, encoding='utf-8')
driver.close()