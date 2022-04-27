# -*- coding: utf-8 -*-
"""preprocess.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mHTPa8SL-A3N_8zGuMuYQE74dhRUD-s6
"""

import numpy as np
import pandas as pd
import json
import ast
from tqdm import tqdm
import pandas as pd
import numpy as np
import nltk
nltk.download('reuters')
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.corpus import reuters
from emot.emo_unicode import UNICODE_EMOJI # For emojis
from emot.emo_unicode import EMOTICONS_EMO # For EMOTICONS
import matplotlib.pyplot as plt
import seaborn as sns
import emoji
import sklearn
import re

crypto = "ShibaInu"

dataframe = pd.read_excel(f"{crypto}_tweet_crypto.xlsx")
dataframe.head(3)

dataframe.columns

arr = np.squeeze(np.array(dataframe["User"].apply(pd.Series)))
dataArray = []
for i in tqdm(range(len(arr))):
    dict = ast.literal_eval(arr[i])
    json_string = json.dumps(dict) 
    newData = json.loads(json_string)
    f1 = pd.json_normalize(newData)
    dataArray.append(f1)

user_id_str_list = []
user_name_list = []
user_f_count_list = []
user_verif = []
for i in tqdm(range(len(arr))):
    id_str = dataArray[i]['id_str']
    name = dataArray[i]['name']
    f_cnt = dataArray[i]['followers_count']
    verif = dataArray[i]['verified']
    user_id_str_list.append(id_str)
    user_name_list.append(name)
    user_f_count_list.append(f_cnt)
    user_verif.append(verif)

dataframe['user_id_str'] = np.array(user_id_str_list)
dataframe['user_name'] = np.array(user_name_list)
dataframe['user_followers_count'] = np.array(user_f_count_list)
dataframe['user_verified'] = np.array(user_verif)

dataframe.columns

# newUserData = pd.concat(dataArray)
# newUserData = pd.DataFrame(newUserData)
# newUserData.head(3)

# newUserData.shape

# newUserData.columns

# for col in newUserData.columns:
#     newName = "user_"+col
#     newUserData = newUserData.rename(columns = {col: newName})

# newUserData.columns

# for col in newUserData.columns:
#     dataframe[col] = np.array(newUserData[col])

dataframe.shape

reuters = set(nltk.corpus.reuters.words())
my_stopwords = nltk.corpus.stopwords.words('english')
word_rooter = nltk.stem.snowball.PorterStemmer(ignore_stopwords=False).stem
my_punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@'

def find_retweeted(tweet):
    '''This function will extract the twitter handles of retweed people'''
    return re.findall('(?<=RT\s)(@[A-Za-z]+[A-Za-z0-9-_]+)', tweet)
    
def find_mentioned(tweet):
    '''This function will extract the twitter handles of people mentioned in the tweet'''
    return re.findall('(?<!RT\s)(@[A-Za-z]+[A-Za-z0-9-_]+)', tweet)  

def find_hashtags(tweet):
    '''This function will extract hashtags'''
    return re.findall('(#[A-Za-z]+[A-Za-z0-9-_]+)', tweet) 


def remove_links(tweet):
    '''Takes a string and removes web links from it'''
    tweet = re.sub(r'http\S+', '', tweet) # remove http links
    tweet = re.sub(r'bit.ly/\S+', '', tweet) # rempve bitly links
    tweet = tweet.strip('[link]') # remove [links]
    return tweet

def remove_users(tweet):
    '''Takes a string and removes retweet and @user information'''
    tweet = re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet) # remove retweet
    tweet = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet) # remove tweeted at
    return tweet

def clean_tweet(tweet, bigrams=False):
    tweet = remove_users(tweet)
    tweet = remove_links(tweet)
    tweet = tweet.lower() # lower case
    tweet = re.sub('['+my_punctuation + ']+', ' ', tweet) # strip punctuation
    tweet = re.sub('\s+', ' ', tweet) #remove double spacing
    tweet = re.sub('([0-9]+)', '', tweet) # remove numbers
    tweet_token_list = []
    tweet_token_list = [word for word in tweet.split(' ')
                            if word not in my_stopwords] # remove stopwords

    tweet_token_list = [word_rooter(word) if '#' not in word else word
                        for word in tweet_token_list] # apply word rooter

    if bigrams:
        tweet_token_list = tweet_token_list+[tweet_token_list[i]+'_'+tweet_token_list[i+1]
                                            for i in range(len(tweet_token_list)-1)]
    
    tweet = ' '.join(tweet_token_list)
    
    return tweet
    
def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)
    
def convert_emoticons(text):
    for emot in EMOTICONS_EMO:
        text = text.replace(emot, EMOTICONS_EMO[emot].replace(" ","_"))
    return text

def convert_emojis(tweet):
    tweet = emoji.demojize(tweet)
    tweet = tweet.replace(":"," ")
    tweet = ' '.join(tweet.split())
    return tweet

dataframe['text'] = dataframe['text'].apply(str)

dataframe['hashtags'] = dataframe.text.apply(find_hashtags)
dataframe['mentioned'] = dataframe.text.apply(find_mentioned)
dataframe['text'] = dataframe.text.apply(convert_emoticons)

dataframe['clean_tweet'] = dataframe.text.apply(clean_tweet)
dataframe['changed_text'] = dataframe.clean_tweet.apply(convert_emojis)

dataframe.shape

dataframe.to_csv(f'preprocessed_data/{crypto}_combined_preproc.csv', index=False)

kf = pd.read_csv(f'preprocessed_data/{crypto}_combined_preproc.csv')
print(kf.shape)

def conc_tweet_crypto(data1_list,data2_list):
    j=0
    for i in range(len(data2_list)):
      if data2_list[i][5]<pd.to_datetime("2022-04-10 00:00:00+00:00"):
    #     print(data2_list[i][5].day)
        while((data1_list[j][0] - data2_list[i][5])/np.timedelta64(1,'m')<=0):
            j+=1
        data2_list[i] = data2_list[i] + data1_list[j]
        
    return data2_list


data1 = pd.read_csv("/content/drive/MyDrive/IR_Project/Final_Data/Crypto/Minute_Crypto/XRP_data.csv")
data2 = pd.read_excel("/content/drive/MyDrive/IR_Project/Final_Data/Tweets_1_to_7_Apr/Samyak/Full_joined/Ripple_dataset_full.xlsx")

data1['time'] = pd.to_datetime(data1.time)
data2['created_at'] = pd.to_datetime(data2.created_at)
data1_list = data1.values.tolist()
data2_list = data2.values.tolist()
final_data = conc_tweet_crypto(data1_list,data2_list)

df = pd.DataFrame(final_data)
df.columns = ['Unnamed: 0', 'id', 'text', 'favourite_count', 'retweet_count',
      'created_at', 'User', 'place','time', 'high', 'low', 'open', 'volume_from', 'volume_to', 'close']

df['created_at'] = df['created_at'].dt.tz_localize(None)
df['time'] = df['time'].dt.tz_localize(None)
df.to_excel("/content/drive/MyDrive/IR_Project/Final_Data/Tweets_1_to_7_Apr/Samyak/Crypto_Tweets/Ripple_tweet_crypto.xlsx")