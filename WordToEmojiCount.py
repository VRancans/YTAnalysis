import numpy as np
import matplotlib.pyplot as plt
import csv

X_VAL = 200
Y_VAL = 100

youtuber_category = {}
youtuber_gender = {}

with open("filtered-lv-youtube-channels.csv", mode='r', encoding="utf8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        youtuber_category[row["Name"]] = row["Category"]
        youtuber_gender[row["Name"]] = row["Gender"]

#By Category
word_count_total = []
emoji_count_total = []

word_count_music = []
emoji_count_music = []

word_count_news = []
emoji_count_news = []

word_count_entertainment = []
emoji_count_entertainment = []

word_count_people = []
emoji_count_people = []

word_count_film = []
emoji_count_film = []

word_count_howTo = []
emoji_count_howTo = []

word_count_sports = []
emoji_count_sports = []

word_count_comedy = []
emoji_count_comedy = []

word_count_education = []
emoji_count_education = []

# By Gender
word_count_male = []
emoji_count_male = []

word_count_female = []
emoji_count_female = []

word_count_none = []
emoji_count_none = []

with open("lv-youtuber-comments-v5.csv", mode='r', encoding="utf8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        #total
        word_count_total.append(int(row["word_count"]))
        emoji_count_total.append(int(row["emoji_count"]))

        #category
        if youtuber_category[row["youtuber"]] == "Music":
            word_count_music.append(int(row["word_count"]))
            emoji_count_music.append(int(row["emoji_count"]))

        elif youtuber_category[row["youtuber"]] == "News":
            word_count_news.append(int(row["word_count"]))
            emoji_count_news.append(int(row["emoji_count"]))

        elif youtuber_category[row["youtuber"]] == "Entertainment":
            word_count_entertainment.append(int(row["word_count"]))
            emoji_count_entertainment.append(int(row["emoji_count"]))

        elif youtuber_category[row["youtuber"]] == "People":
            word_count_people.append(int(row["word_count"]))
            emoji_count_people.append(int(row["emoji_count"]))

        elif youtuber_category[row["youtuber"]] == "Film":
            word_count_film.append(int(row["word_count"]))
            emoji_count_film.append(int(row["emoji_count"]))

        elif youtuber_category[row["youtuber"]] == "HowTo":
            word_count_howTo.append(int(row["word_count"]))
            emoji_count_howTo.append(int(row["emoji_count"]))

        elif youtuber_category[row["youtuber"]] == "Sports":
            word_count_sports.append(int(row["word_count"]))
            emoji_count_sports.append(int(row["emoji_count"]))

        elif youtuber_category[row["youtuber"]] == "Comedy":
            word_count_comedy.append(int(row["word_count"]))
            emoji_count_comedy.append(int(row["emoji_count"]))

        elif youtuber_category[row["youtuber"]] == "Education":
            word_count_education.append(int(row["word_count"]))
            emoji_count_education.append(int(row["emoji_count"]))

        # gender
        if youtuber_gender[row["youtuber"]] == "Male":
            word_count_male.append(int(row["word_count"]))
            emoji_count_male.append(int(row["emoji_count"]))

        elif youtuber_gender[row["youtuber"]] == "Female":
            word_count_female.append(int(row["word_count"]))
            emoji_count_female.append(int(row["emoji_count"]))

        elif youtuber_gender[row["youtuber"]] == "None":
            word_count_none.append(int(row["word_count"]))
            emoji_count_none.append(int(row["emoji_count"]))

# Total Analysis
fig = plt.figure()

ax = fig.add_subplot(111)
ax.set_xlabel('Word Count')
ax.set_ylabel('Emoji Count')
ax.set_xlim([-8,X_VAL])
ax.set_ylim([-4,Y_VAL])

plt.title('Word To Emoji Ratio')

ax.scatter(word_count_total,emoji_count_total, edgecolor='black', linewidths=0.2, alpha=0.5, s=20)

# Analysis By Category
fig = plt.figure()

ax = fig.add_subplot(331)
ax.set_xlabel('Word Count')
ax.set_ylabel('Emoji Count')
ax.set_xlim([-8,X_VAL])
ax.set_ylim([-4,Y_VAL])
plt.title('Word To Emoji Ratio (MUSIC)')
ax.scatter(word_count_music,emoji_count_music, edgecolor='black', linewidths=0.2, alpha=0.5, s=20)

ax = fig.add_subplot(332)
ax.set_xlabel('Word Count')
ax.set_ylabel('Emoji Count')
ax.set_xlim([-8,X_VAL])
ax.set_ylim([-4,Y_VAL])
plt.title('Word To Emoji Ratio (NEWS)')
ax.scatter(word_count_news,emoji_count_news, edgecolor='black', linewidths=0.2, alpha=0.5, s=20)

ax = fig.add_subplot(333)
ax.set_xlabel('Word Count')
ax.set_ylabel('Emoji Count')
ax.set_xlim([-8,X_VAL])
ax.set_ylim([-4,Y_VAL])
plt.title('Word To Emoji Ratio (ENTERTAINMENT)')
ax.scatter(word_count_entertainment,emoji_count_entertainment, edgecolor='black', linewidths=0.2, alpha=0.5, s=20)

ax = fig.add_subplot(334)
ax.set_xlabel('Word Count')
ax.set_ylabel('Emoji Count')
ax.set_xlim([-8,X_VAL])
ax.set_ylim([-4,Y_VAL])
plt.title('Word To Emoji Ratio (PEOPLE)')
ax.scatter(word_count_people,emoji_count_people, edgecolor='black', linewidths=0.2, alpha=0.5, s=20)

ax = fig.add_subplot(335)
ax.set_xlabel('Word Count')
ax.set_ylabel('Emoji Count')
ax.set_xlim([-8,X_VAL])
ax.set_ylim([-4,Y_VAL])
plt.title('Word To Emoji Ratio (FILM)')
ax.scatter(word_count_film,emoji_count_film, edgecolor='black', linewidths=0.2, alpha=0.5, s=20)

ax = fig.add_subplot(336)
ax.set_xlabel('Word Count')
ax.set_ylabel('Emoji Count')
ax.set_xlim([-8,X_VAL])
ax.set_ylim([-4,Y_VAL])
plt.title('Word To Emoji Ratio (HOWTO)')
ax.scatter(word_count_howTo,emoji_count_howTo, edgecolor='black', linewidths=0.2, alpha=0.5, s=20)

ax = fig.add_subplot(337)
ax.set_xlabel('Word Count')
ax.set_ylabel('Emoji Count')
ax.set_xlim([-8,X_VAL])
ax.set_ylim([-4,Y_VAL])
plt.title('Word To Emoji Ratio (SPORTS)')
ax.scatter(word_count_sports,emoji_count_sports, edgecolor='black', linewidths=0.2, alpha=0.5, s=20)

ax = fig.add_subplot(338)
ax.set_xlabel('Word Count')
ax.set_ylabel('Emoji Count')
ax.set_xlim([-8,X_VAL])
ax.set_ylim([-4,Y_VAL])
plt.title('Word To Emoji Ratio (COMEDY)')
ax.scatter(word_count_comedy,emoji_count_comedy, edgecolor='black', linewidths=0.2, alpha=0.5, s=20)

ax = fig.add_subplot(339)
ax.set_xlabel('Word Count')
ax.set_ylabel('Emoji Count')
ax.set_xlim([-8,X_VAL])
ax.set_ylim([-4,Y_VAL])
plt.title('Word To Emoji Ratio (EDUCATION)')
ax.scatter(word_count_education,emoji_count_education, edgecolor='black', linewidths=0.2, alpha=0.5, s=20)


# Analysis By Gender
fig = plt.figure()

ax = fig.add_subplot(221)
ax.set_xlabel('Word Count')
ax.set_ylabel('Emoji Count')
ax.set_xlim([-8,X_VAL])
ax.set_ylim([-4,Y_VAL])
plt.title('Word To Emoji Ratio (MALE)')
ax.scatter(word_count_male,emoji_count_male, edgecolor='black', linewidths=0.1, alpha=0.2, s=20)

ax = fig.add_subplot(222)
ax.set_xlabel('Word Count')
ax.set_ylabel('Emoji Count')
ax.set_xlim([-8,X_VAL])
ax.set_ylim([-4,Y_VAL])
plt.title('Word To Emoji Ratio (FEMALE)')
ax.scatter(word_count_female,emoji_count_female, edgecolor='black', linewidths=0.1, alpha=0.2, s=20)

ax = fig.add_subplot(223)
ax.set_xlabel('Word Count')
ax.set_ylabel('Emoji Count')
ax.set_xlim([-8,X_VAL])
ax.set_ylim([-4,Y_VAL])
plt.title('Word To Emoji Ratio (NONE)')
ax.scatter(word_count_none,emoji_count_none, edgecolor='black', linewidths=0.1, alpha=0.2, s=20)

plt.show()