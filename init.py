import praw
from keys import keys
from config import config

# REST API connection
reddit = praw.Reddit(client_id=keys['client_id'],
                     client_secret=keys['client_secret'],
                     user_agent=keys['user_agent'],
                     username=keys['username'],
                     password=keys['password'])

f = open('copiedPostIds.txt', 'r')
postedIds = f.read().lower().splitlines()
f.close()

for submission in reddit.subreddit(config['fromSub']).stream.submissions():
    if config['postTitleIncludes'] in submission.title:
        if submission.id not in postedIds:
            f = open('copiedPostIds.txt', 'a+')
            f.write(str(submission.id))
            f.close()
            postedIds.append(str(submission.id))

            submission.crosspost(config['toSub'], title=submission.title, send_replies=True)
            print("Crossposted \n\t" + submission.title)
