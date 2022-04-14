from config import *
import tweepy
import datetime
#from datetime import datetime
import time

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True)


Number_of_Days = 3


today = datetime.date.today() - datetime.timedelta(days=Number_of_Days)
yesterday= today - datetime.timedelta(days=(1))
print(yesterday)
cryptox = { 'Solana_dataset_new':['Solana'], 'Ripple_dataset_new':['Ripple'], 'Avalanche_dataset_new':['Avalanche'], 'DogeCoin_dataset_new' : ['Dogecoin'], 'Matic_dataset_new' : ['Matic'], 'ShibaInu_dataset_new' : ['Shiba']}
crypto = {  'Matic_dataset_new' : ['Matic']}

for i in cryptox:
    output = []
    for j in cryptox[i]:
        tweets_list = tweepy.Cursor(api.search_tweets, q=j+" -filter:retweets since:" + str(yesterday)+ " until:" + str(today),tweet_mode='extended', lang='en').items()
        print(tweets_list)
        while True:
            try:
                for tweet in tweets_list:
                    
                    id = tweet.id
                    text = tweet._json["full_text"]
                    #print(id)
                    favourite_count = tweet.favorite_count
                    retweet_count = tweet.retweet_count
                    created_at = tweet.created_at
                    user = tweet._json["user"]
                    place = tweet._json["place"]
                    print(j,created_at)
                    line = {'id' : id, 'text' : text, 'favourite_count' : favourite_count, 'retweet_count' : retweet_count, 'created_at' : created_at, 'User' : user, 'place' : place}
                    output.append(line)
                break
            except tweepy.errors.TweepyException as e:
                print(str(e))
            print("sleeping")
            time.sleep(5)


    import pandas as pd
    df = pd.DataFrame(output)
    df.to_csv(i+'.csv', mode='a', header = True)