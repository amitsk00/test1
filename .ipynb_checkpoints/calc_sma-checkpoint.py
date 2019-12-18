#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 19:21:18 2018

@author: amitk
"""


import os
import pandas as pd
cwd = '              '


def check_date_absent(processing_date):
    global cwd
    
    df = pd.read_csv(cwd + '/data/25-08-2017-TO-24-08-2018SBINALLN.csv')
    return df.index[df["Date"] == processing_date].empty


def read_historical_data(processing_date, days, field_name):
    global cwd
    
    df = pd.read_csv(cwd + '/data/25-08-2017-TO-24-08-2018SBINALLN.csv')
    processing_date_row_index = df.index[df["Date"] == processing_date].values[0]
    if days < 0 and processing_date_row_index < abs(days):
        raise ValueError('Date is lesser than threshold to process', field_name)
    elif days > 0 and processing_date_row_index > df.index[-1]-10:
        raise ValueError('Date is greater than threshold to process', field_name)

    if int(days) < 0:
        df1 = df[processing_date_row_index + days: processing_date_row_index]
    else:
        df1 = df[processing_date_row_index + 1: processing_date_row_index + days + 1]

    return df1[field_name].values.tolist()


def current_date_data(processing_date):
    global cwd
    
    df = pd.read_csv(cwd + '/data/25-08-2017-TO-24-08-2018SBINALLN.csv')
    return df[df["Date"] == processing_date]


def cal_sma_volume(processing_date, days):
    last_days_volume = read_historical_data(processing_date, days, 'Total Traded Quantity')
    last_days_volume = map(int, last_days_volume)
    return sum(last_days_volume) / abs(days)


def cal_sma_price(processing_date, days):
    next_days_price = read_historical_data(processing_date, days, 'Average Price')
    next_days_price = map(float, next_days_price)
    return sum(next_days_price) / abs(days)


def main():
    global cwd
    
    current_date = "28-Mar-2018"
    sma_volume_days = -5
    sma_price_days = 10
    
    cwd = os.getcwd()
    print (cwd + '/data/25-08-2017-TO-24-08-2018SBINALLN.csv')
    print (__file__)

    #Indicator 1
    df = pd.read_csv(cwd + '/data/25-08-2017-TO-24-08-2018SBINALLN.csv')
    prediction_result = []
    for index, row in df.iterrows():
        current_date = row['Date']

        try:
            if check_date_absent(current_date):
                print('Data doesn\'t exist for this date')
                exit(0) #use continue when in loop

            sma_volume = cal_sma_volume(current_date, sma_volume_days)
            current_df = current_date_data(current_date)
            # print('SMA Volume:', sma_volume)
            # print('Today avg price', current_df['Average Price'].values[0])
            # print (current_df['Close Price'].values[0], current_df['Open Price'].values[0])
            # print (float(current_df['Total Traded Quantity']))

            if ((current_df['Close Price'] > current_df['Open Price']).values[0]) and (float(current_df['Total Traded Quantity']) > sma_volume):
                indicator1_suggestion = 'Buy'
            elif ((current_df['Close Price'] < current_df['Open Price']).values[0]) and (float(current_df['Total Traded Quantity']) > sma_volume):
                indicator1_suggestion = 'Sell'
            else:
                indicator1_suggestion = 'NA'

            sma_price = cal_sma_price(current_date, sma_price_days)
            assertion_correctness = False
            if indicator1_suggestion == 'Buy':
                if sma_price > current_df['Average Price'].values[0]:
                    assertion_correctness = True
                    # print('Prediction was correct: ', current_date, indicator1_suggestion)
                else:
                    assertion_correctness = False
                    # print('Prediction was not correct: ', current_date, indicator1_suggestion)
            if indicator1_suggestion == 'Sell':
                if sma_price < current_df['Average Price'].values[0]:
                    assertion_correctness = True
                    # print('Prediction was correct: ', current_date, indicator1_suggestion)
                else:
                    assertion_correctness = False
                    # print('Prediction was not correct: ', current_date, indicator1_suggestion)

            prediction_result.append((current_date, indicator1_suggestion, assertion_correctness))
        except Exception as error:
            print('Caught this error: ' + repr(error))

    # print(prediction_result)
    results = pd.DataFrame(prediction_result)
    # print(results)
    print(results.groupby([2]).count())


if __name__ == "__main__":
    main()

