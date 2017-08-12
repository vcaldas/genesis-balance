#!/usr/bin/env python3
"""
Created on Sat Aug 12 20:26:40 2017

@author: caldas
"""
#from selenium import webdriver
#driver = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
#
#url = "https://www.youraddress.com"
#
#driver.execute_script("window.open(url,"_self");")  <--- JAVASCRIPT!
#("window.open('');")


from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime as dt
import pandas as pd

# Creating dataframe to save data.
columns = ["date", "coin", "value", "wallet", "paid"]
col_names_payout = ['total', 'paid', 'balance', 'last payment', 'last payout' ]


df = pd.DataFrame(columns = columns)

url = "https://www.genesis-mining.com/transactions/index/page"
driver = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
driver.get("https://www.genesis-mining.com/en")


def append_data(soup, df):
    transactions = soup.find("div", {"id": "my-transactions"})
    table = transactions.find('table', attrs={'class':'table'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        df = df.append({'date': cols[0], 'coin': cols[1], 'value': cols[2][:10], 'wallet': cols[3], 'hash': cols[4]}, ignore_index=True)
    return df


try:
    element = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, "current-mining"))
    )
finally:
    # Get number of pages to loop through
    print("Parsing page %s." % 1)
    driver.get(url+str(1))
    source = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(source, 'html.parser')
    
    pages = str(soup.findAll("p", { "class" : "pager-info" }))
    start = pages.find("Page 1 of ")
    end = pages.find(", showing" )
    npages =  int(pages[start+10: end])
    
   
    for current in range(1, npages):
        print("Parsing page %s out of %s." % (current, npages))
        driver.get(url+str(current))
        
        source = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(source, 'html.parser')
        df = append_data(soup, df)
       
        
    
driver.quit()

### Working on Dataframe

df['date'] = pd.to_datetime(df['date'])
df['date'] = df['date'].apply(lambda x: dt.datetime.strftime(x, '%d-%m-%Y'))

#df.paid = df.paid.apply(lambda x: True if x == "View Transaction" else False)

# Get all coins
my_coins = df.coin.unique()
print(my_coins)

# Create a new dataframe
payouts = pd.DataFrame(index = df.coin.unique(), columns = col_names_payout)

## add values to the payout dataframe
#for row in payouts.iterrows():
#    coin =  row[0]; 
#    my_df  = df.loc[df.coin == coin]
#     
#   
#    payouts.set_value(coin, 'total', my_df.payout.sum())
#    
#    paid = df.payout.loc[(df.coin == coin) & (df.paid == True)].sum()
#
#    payouts.set_value(coin, 'value', my_df.payout.loc[my_df.paid == True].sum())
#    
#    payouts.set_value(coin, 'last payment', my_df.date.max())
#
#    payouts.set_value(coin, 'last payout',  my_df.loc[my_df.paid == True].date.max())
#    
#    
#payouts.balance = payouts.total - payouts.paid


print(df)
print(payouts)

## save df
#with open("source.csv", "wb") as f:
df.to_csv("source.csv")
#    
#with open("payouts.csv", "wb") as f:
payouts.to_csv("payouts.csv")




    