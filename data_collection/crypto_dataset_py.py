# -*- coding: utf-8 -*-
"""crypto_dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Nzi5EnHpS6vSYvmWe2p_NN5SHhr8Oy_8
"""

import requests

# importing datetime module
import datetime
import time
import json
import pandas as pd
import csv

def convert_to_datetime(unix_time):
    dt = datetime.datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%SZ')
    s = dt[:10] + ' ' + dt[11:len(dt) - 1] + '+00:00'
    return s

date_time = datetime.datetime(2022, 4, 9, 5, 30)
unix_time = unix_time = int(time.mktime(date_time.timetuple()))

currencies = ['SHIB', 'DOGE', 'XRP', 'AVAX', 'MATIC', 'SOL']

cols = ['time', 'high', 'low', 'open', 'volume_from', 'volume_to', 'close']
for curr in currencies:
    print(f"Currency = {curr}")
    currency_output = []
    # f = json.load(open(f'{curr}_data.json'))
    query_str = f"https://min-api.cryptocompare.com/data/v2/histominute?fsym={curr}&tsym=USD&limit=1440&toTs={unix_time}"
    response = requests.get(query_str)
    f = response.json()
    data = f['Data']
    time_from = convert_to_datetime(data['TimeFrom'])
    time_to = convert_to_datetime(data['TimeTo'])
    print(f"Data from {time_from} till {time_to}")
    price_data = data['Data']
    print(f"Num_record = {len(price_data)}")
    for rec in price_data:
        entry = [convert_to_datetime(rec['time']), rec['high'], rec['low'], rec['open'], rec['volumefrom'], rec['volumeto'], rec['close']]
        currency_output.append(entry)
    currency_output = currency_output[:len(currency_output) - 1]
    print(f"num rows = {len(currency_output)}")
    print(f"First data point = {currency_output[0]}")
    print(f"Last data point = {currency_output[len(currency_output) - 1]}")
    # print(currency_output[len(currency_output) - 1])
    with open(f"./CryptoData/{curr}_data.csv",'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(currency_output)
    
    print("\n------------------------\n")