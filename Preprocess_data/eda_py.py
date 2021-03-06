# -*- coding: utf-8 -*-
"""eda.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SWYLAvzSDcINMKFX2Cimo0AL2o8Q5HFs
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
from wordcloud import WordCloud
from matplotlib import pyplot as plt

# Solana  ,   Avalanche  ,  DogeCoin  ,  Matic  , ShibaInu

crypto = "Avalanche"

df = pd.read_csv(f'./preprocessed_data/{crypto}_combined_preproc.csv')

print(df.shape)

df.columns

string = []
for t in df['changed_text']:
    string.append(t)
token_set = set()
for sent in string:
    # print(sent)
    sent = str(sent)
    # print(type(sent))
    toks = list(sent.split(' '))
    for tok in toks:
        token_set.add(tok)
token_set = list(token_set)
string = list(set(string))
string = pd.Series(token_set).str.cat(sep=' ')

wordcloud = WordCloud(width=1600, height=800,max_font_size=200).generate(string)
plt.figure(figsize=(12,10))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig(f'./eda_results/wordcloud_{crypto}')
plt.show()

print(df.shape)
df.shape[0]

"""Tweet Counts"""

coins = ['avax', 'doge', 'matic','shiba', 'solana']

df_avax = pd.read_csv("./preprocessed_data/Avalanche_combined_preproc.csv")
df_doge = pd.read_csv("./preprocessed_data/DogeCoin_combined_preproc.csv")
df_matic = pd.read_csv("./preprocessed_data/Matic_combined_preproc.csv")
# df_ripple = pd.read_csv("./preprocessed_data/Ripple_combined_preproc.csv")
df_shib = pd.read_csv("./preprocessed_data/ShibaInu_combined_preproc.csv")
df_sol = pd.read_csv("./preprocessed_data/Solana_combined_preproc.csv")

counts = {'avax': df_avax.shape[0], 'doge': df_doge.shape[0], 'matic': df_matic.shape[0], 'shiba': df_shib.shape[0], 'solana': df_sol.shape[0]}

counts_df = pd.DataFrame(counts.items(), columns=['crypto coin','#tweets'])
counts_df[counts_df.columns[::-1]]

counts_df

counts_df.loc[counts_df["crypto coin"] == "avax", "#tweets"] = 22229

sns.set_theme(style="whitegrid")
# tips = sns.load_dataset("tips")
ax = sns.barplot(x="crypto coin", y="#tweets", data=counts_df)
plt.savefig("./eda_results/tweet_counts.png", bbox_inches='tight', facecolor='w')

df_avax['lens'] = df_avax['text'].apply(lambda x: len(str(x)))
df_doge['lens'] = df_doge['text'].apply(lambda x: len(str(x)))
df_matic['lens'] = df_matic['text'].apply(lambda x: len(str(x)))
df_shib['lens'] = df_shib['text'].apply(lambda x: len(str(x)))
df_sol['lens'] = df_sol['text'].apply(lambda x: len(str(x)))

lens = {'avax': df_avax['lens'].sum() / df_avax.shape[0], 'doge': df_doge['lens'].sum() / df_doge.shape[0], 'matic': df_matic['lens'].sum() / df_matic.shape[0], 'shiba': df_shib['lens'].sum() / df_shib.shape[0], 'solana': df_sol['lens'].sum() / df_sol.shape[0]}

lens_df = pd.DataFrame(lens.items(), columns=['crypto coin','Avg. Tweet Length'])
lens_df[lens_df.columns[::-1]]
lens_df = lens_df.astype({'Avg. Tweet Length':'int'})

lens_df

overall_avg = sum(lens.values()) / 5
overall_avg

sns.set_theme(style="whitegrid")
# tips = sns.load_dataset("tips")
ax = sns.barplot(x="crypto coin", y="Avg. Tweet Length", data=lens_df)
ax.bar_label(ax.containers[0])
plt.savefig("./eda_results/tweet_lens.png", bbox_inches='tight', facecolor='w')