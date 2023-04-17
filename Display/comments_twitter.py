import snscrape.modules.twitter as sntwitter
import pandas as pd

# Creating list to append tweet data to
tweets_list2 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:aajtak पुलिस lang:hi since:2023-01-01 until:2023-03-31 include:replies').get_items()):
    if i>10:
        break
    tweets_list2.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
    
# Creating a dataframe from the tweets list above
tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
tweets_df2.to_csv('tweets.csv')
print(tweets_df2['Text'])

# query = 'lang:ur' #ur is code for urdu
# #limit = 10
# urduTweets = sntwitter.TwitterSearchScraper(query).get_items()
# print(urduTweets)