#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 16:45:45 2018

@author: amitk
"""


import os
import pandas as pd
cwd = ' '

def check_ema():
    global ind
    
    #print (ind)
    #s1 = ind["ema_5"].values(0) 
    #s0 = ind["p_symbol"]
    #s1 = ind["ema_5"]
    #s2 = ind["ema_13"]
    #s3 = ind["ema_34"]
    #s_fin = pd.concat([s0,s1,s2,s3], axis=1)
    #print (s_fin)
    
    for index, row in ind.iterrows():
        if (row['ema_5'] > row['ema_13']) and (row['ema_13'] > row['ema_34']) and (row['ema_34'] > row['ema_50']):
            flag_ema = 'BUY'
        elif (row['ema_5'] < row['ema_13']) and (row['ema_13'] < row['ema_34']) and (row['ema_34'] < row['ema_50']):
            flag_ema = 'SELL'
        else:
            flag_ema = 'NA'
        ind['ind_ema'].iloc[index] = flag_ema
        
        
def add_columns ():
    ind['ind_ema'] = 'X' 

def read_file ():
    global cwd
    global ind
    
    cwd = os.getcwd()
    data_file = cwd + '/symbol_indicators.csv'
    #print (data_file)
    #print (__file__)
    
    ind = pd.read_csv(data_file, header=0)




def main ():
    read_file ()
    add_columns ()
    check_ema ()
    
    #print (ind[ind['ind_ema'] == 'BUY'])
    print(ind)

if __name__ == "__main__":
    main()

