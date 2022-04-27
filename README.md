# Analysing Cryptocurrrency trends using Tweet Sentiment Data and User Meta-Data

This project is part of Information Retrieval - Winter 2022 course.

# Project Description

We captured sentiments of text in the tweets to analyse the effect of tweet sentiments on the price of the cryptocurrency and then incorporated user-meta data to conclude the fluctuation. We combine and use all the features to then predict the price of these cryptocurrencies.

# Dataset

We captured the twitter data using tweepy API and cryptocurrency data using CryptoComapare API.
Google Drive Link for pickle files and dataset: https://drive.google.com/drive/folders/1aHgbSDKVDgXVxJEgrgeahkiRb4j6pd-T?usp=sharing

# Pre-Processing

Preprocessing was done on various aspects of the tweets to create a plain text & clean dataset. Then the dataset of crypto and tweets was combined for further time series analysis.

# Sentiment Analysis
We did Sentiment analysis as NLP task to categorise the opinions in the given text. Further, we fine tuned a previous sentiment analysis model to improve sentiment results.

# Models
We used Regressor models and then LSTM model to analysis the crypto data using the sentiments generated for tweets data along with tweet and related user metadata.

![model_architecture](https://user-images.githubusercontent.com/64920972/165535784-7760b9af-3014-4b3c-9146-2ea0cd6b8b97.jpeg)


# Libraries Required

```
$ pip install Sklearn
$ pip install numpy
$ pip install pandas
$ pip install matplotlib
$ pip install WordCloud
$ pip install tqdm
$ pip install nltk
$ pip install torch
$ pip install torchvision
$ pip install torchaudio
$ pip install emoji
$ pip install emot 
$ pip install seaborn
$ pip install tweepy
$ pip install datasets
$ pip install transformers
$ pip install hugginggace_hub
$ pip install requests
$ pip install scipy
```
