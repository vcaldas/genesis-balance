#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 12:42:42 2017

@author: Victor Caldas
"""

# Genesis Payout report


import argparse
import pandas as pd
import datetime as dt


parser = argparse.ArgumentParser()
parser.add_argument('filename', help='A csv file')
args = parser.parse_args()


col_names = ('date', 'coin', 'payout', 'wallet',  'paid')
col_names_payout = ['total', 'paid', 'balance', 'last payment', 'last payout' ]


#Import file
df = pd.read_csv(args.filename, sep= '\t', names = col_names)




df['date'] = pd.to_datetime(df['date'])
df['date'] = df['date'].apply(lambda x: dt.datetime.strftime(x, '%d-%m-%Y'))

# Remove annoying i from payouts
df.payout = df.payout.apply(lambda x : float(x.replace("i", "")))

# When there is "View Transaction" , it means that the balance is pay. Change for
# paid : True,False
df.paid = df.paid.apply(lambda x: True if x == "View Transaction" else False)

# Get all coins
my_coins = df.coin.unique()

    
# Create a new dataframe
payouts = pd.DataFrame(index = df.coin.unique(), columns = col_names_payout)

## add values to the payout dataframe
for row in payouts.iterrows():
    coin =  row[0]; 
    my_df  = df.loc[df.coin == coin]
     
   
    payouts.set_value(coin, 'total', my_df.payout.sum())
    
    paid = df.payout.loc[(df.coin == coin) & (df.paid == True)].sum()

    payouts.set_value(coin, 'paid', my_df.payout.loc[my_df.paid == True].sum())
    
    payouts.set_value(coin, 'last payment', my_df.date.max())

    payouts.set_value(coin, 'last payout',  my_df.loc[my_df.paid == True].date.max())
    
    
payouts.balance = payouts.total - payouts.paid

print(payouts)
