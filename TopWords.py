import numpy as np
import matplotlib.pyplot as plt
import csv
import emoji
import re
from collections import Counter

MIN_WORD_LENGTH = 4

def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(r'', text)

youtubers = []
videos = []
words = []
video_id = None
channel_id = None

with open("lv-youtuber-comments-v5.csv", mode='r', encoding="utf8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if row["youtuber"] not in youtubers:
            youtubers.append(row["youtuber"])
        if row["title"] not in videos:
            videos.append(row["title"])

print("1. Analyse all comments\n2. Analyse specific Channel\n3. Analyse specific video")
choice = input("Enter the number of the action you want to take!\n")

while not(choice.isdigit() and int(choice) >= 1 and int(choice) <= 3):
    choice = input("Could not understand! Please pick one of the offered options!\n")

choice = int(choice)
if choice == 1:
    with open("lv-youtuber-comments-v5.csv", mode='r', encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            emojiless_comment = remove_emoji(row["comment"])
            for word in re.findall(r'\w+', emojiless_comment):
                if len(word) >= MIN_WORD_LENGTH:
                    words.append(word.lower())

elif choice == 2:
    for idx, item in enumerate(youtubers):
        print(str(idx + 1) + ". " + item)

    channel_id = input("Which channel would you like to analyse?\n")
    while not (channel_id.isdigit() and int(channel_id) >= 1 and int(channel_id) <= len(youtubers)):
        channel_id = input("Could not understand! Please pick one of the offered options!\n")

    channel_id = int(channel_id)
    with open("lv-youtuber-comments-v5.csv", mode='r', encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            if row["youtuber"] == youtubers[int(channel_id) - 1]:
                emojiless_comment = remove_emoji(row["comment"])
                for word in re.findall(r'\w+', emojiless_comment):
                    if len(word) >= MIN_WORD_LENGTH:
                        words.append(word.lower())
elif choice == 3:
    print(1)
    for idx, item in enumerate(videos):
        print(str(idx + 1) + ". " + item)

    video_id = input("Which video would you like to analyse?\n")
    while not (video_id.isdigit() and int(video_id) >= 1 and int(video_id) <= len(videos)):
        video_id = input("Could not understand! Please pick one of the offered options!\n")

    video_id = int(video_id)
    with open("lv-youtuber-comments-v5.csv", mode='r', encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            if row["title"] == videos[int(video_id) - 1]:
                emojiless_comment = remove_emoji(row["comment"])
                for word in re.findall(r'\w+', emojiless_comment):
                    if len(word) >= MIN_WORD_LENGTH:
                        words.append(word.lower())

top_words = dict(Counter(words).most_common(20))
print(top_words)

plt.figure()
plt.xlabel('Word')
plt.ylabel('Times found in comments')
plt.xticks(rotation=-30)
if choice == 2:
    plt.title('Popular words for channel "%s"' % youtubers[channel_id - 1])
elif choice == 3:
    plt.title('Popular words for video "%s"' % videos[video_id - 1])
else:
    plt.title('Most popular words for collected data')

plt.bar(top_words.keys(), top_words.values(), align='center')
plt.show()