import requests
import json
import praw
import pandas
import datetime
import time
import nltk

# Get unix timestamp of 24hrs ago
last24hours = datetime.datetime.now() - datetime.timedelta(days=1)
last24hours_unix = time.mktime(last24hours.timetuple())

# Load auth information from config.json
with open("config.json") as json_data_file:
    auth_data = json.load(json_data_file)

# Create a reddit instance
reddit = praw.Reddit(client_id=auth_data["login"]["client_id"],
                     client_secret=auth_data["login"]["client_secret"],
                     user_agent=auth_data["login"]["user_agent"],
                     username=auth_data["login"]["username"],
                     password=auth_data["login"]["password"])

# Set subreddit
subreddit = reddit.subreddit("wallstreetbets")

# Create dataframe instance
df = pandas.DataFrame()

# Loop through post and filter if under 24hr
for submission in subreddit.new(limit=999):
    if submission.created_utc > last24hours_unix:
        df = df.append({
            'title': submission.title,
            'selftext': submission.selftext,
            'created_utc': datetime.datetime.fromtimestamp(submission.created_utc).strftime('%d-%m-%Y %H:%M:%S'),
            'upvote_ratio': submission.upvote_ratio,
            'score': submission.score,
            'ups': submission.ups,
            'downs': submission.downs
        }, ignore_index=True)

print(df)
