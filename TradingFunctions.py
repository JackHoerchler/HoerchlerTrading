
import alpaca_trade_api as tradeapi
import requests, json
import yfinance as yf

############################################################################## Alpaca Functions##############################################################################

API_KEY = 'PKJ3Q8EE6CGAIP22C7SR'
SECRET_KEY = 'pjJqsLDaI8lB1zqOIdONsdtGKISjzyoMkR4GxG36'

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)

HEADERS = {'APCA-API-KEY-ID': API_KEY,'APCA-API-SECRET-KEY': SECRET_KEY}
api = tradeapi.REST(API_KEY,SECRET_KEY)


def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(r.content)


def create_order(symbol , qty, side, typ, time_in_force):
   
    data = {
        "symbol" : symbol,
        "qty" : qty,
        "side" : side,
        "type" : typ,
        "time_in_force" : time_in_force        
        }
   
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)    
    return json.loads(r.content)


def get_orders():
    r = requests.get(ORDERS_URL, headers=HEADERS)
   
    #print(r.content)
   
    return json.loads(r.content)
   

def get_market_open():
    # Check if the market is open now.
    clock = api.get_clock()
    return clock.is_open

############################################################################## CSV functions##############################################################################

import csv


def update_symbols():
    symbols = []
    with open('Symbols.csv') as csv_file:
        
        csv_reader = csv.reader(csv_file,delimiter=',')
        
        for row in csv_reader:
            symbols.append(row[0])
            
    symbols.pop(0)
    return(symbols)
        
############################################################################## Live Price Function##############################################################################

import bs4


def get_live_price(symbol):
    
    site = 'https://finance.yahoo.com/quote/' +  str(symbol) + '?p=' + str(symbol)
    
    r=requests.get(site)
    soup = bs4.BeautifulSoup(r.text,"lxml")

    price = soup.find('div',{'class':'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    
    return price

############################################################################## yahoofinance function##############################################################################

def get_volume(symbol):
    data = yf.Ticker(symbol)
    return data.info['volume']   

def get_average_volume(symbol):
    data = yf.Ticker(symbol)
    return data.info['averageVolume']

def get_10_day_average_volume(symbol):
    data = yf.Ticker(symbol)
    return data.info['averageVolume10days']    

def get_regular_market_price(symbol):
    data = yf.Ticker(symbol)
    return data.info['regularMarketPrice']


def get_current_ask_price(symbol):
    data = yf.Ticker(symbol)
    return data.info['ask']

def get_current_bid_price(symbol):
    data = yf.Ticker(symbol)
    return data.info['bid']

############################################################################## yahoofinance historicaldata##############################################################################

import pandas as pd
import ts_charting as charting
import pandas.io.data as pdd

from datetime import date,timedelta


#finds the last 5 business days

def get_historical_data(symbol,weekdays,interval):
    
    today = date.today()
    yesterday = today + timedelta(days=-1)

    data = yf.Ticker(symbol)

    weekdata = data.history(period=weekdays,interval=interval,end=yesterday)
    
    return weekdata




test = get_historical_data("MSFT",'5d','1m')


test.plot(y=["High","Low"])

test.ohlc_plot()

print(test['Open']) 


############################################################################## price alert email##############################################################################

def price_alert_email(symbol,GtLt,price,sendee):
    
    if get_market_open():
            
        Price_String =get_live_price(symbol)
        Price_Float = float(get_live_price(symbol))
           
        if(GtLt == '>'):
            flipper = 1
        if(GtLt == '<'):
            flipper = 0
            
            
        if((Price_Float > price and flipper == 1) or (Price_Float < price and flipper == 0)):
            volume = get_volume(symbol)
            tenDayVolume = get_10_day_average_volume(symbol)
            
            moreless = 'higher'
            percent = round(((volume/tenDayVolume)*100-100),2)
            
            if volume < tenDayVolume:
                moreless = 'lower'
                percent = round((100-(volume/tenDayVolume)*100),2)
                
            message1 = symbol + ' stock price is now at $' + str(Price_String) + '.'
            message2 = 'The volume currently traded is ' + str(percent) + '% ' + moreless + ' than the 10 day average.' 
            
            print(message1)
            print(message2)
            
            if(sendee == 'joe'):
                send_email_to_joe(message1,message2)
            if(sendee == 'jack'):
                send_email_to_jack(message1,message2)   
                
            return True
            
        else:
            print(symbol + ' stock price is now at $' + str(Price_String) + '.')
            return False
            
    else:
        print('market closed') 
        return False

############################################################################## send emails##############################################################################

import smtplib


def send_email_to_joe(sub,bod):
    sender_address = "alpacaalert408@gmail.com" # Replace this with your Gmail address
    receiver_address = "joehoerchler@gmail.com" # Replace this with any valid email address
    account_password = "JoeTrade2021" # Replace this with your Gmail account password
 
    subject = sub 
    body = bod
 
    # Endpoint for the SMTP Gmail server (Don't change this!)
    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
     
    # Login with your Gmail account using SMTP
    smtp_server.login(sender_address, account_password)
     
    # Let's combine the subject and the body onto a single message
    message = f"Subject: {subject}\n\n{body}"
 
    # We'll be sending this message in the above format (Subject:...\n\nBody)
    smtp_server.sendmail(sender_address, receiver_address, message)
     
    # Close our endpoint
    smtp_server.close()
    

def send_email_to_jack(sub,bod):
    sender_address = "alpacaalert408@gmail.com" # Replace this with your Gmail address
    receiver_address = "jhoerchler@gmail.com" # Replace this with any valid email address
    account_password = "JoeTrade2021" # Replace this with your Gmail account password
 
    subject = sub 
    body = bod
 
    # Endpoint for the SMTP Gmail server (Don't change this!)
    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
     
    # Login with your Gmail account using SMTP
    smtp_server.login(sender_address, account_password)
     
    # Let's combine the subject and the body onto a single message
    message = f"Subject: {subject}\n\n{body}"
 
    # We'll be sending this message in the above format (Subject:...\n\nBody)
    smtp_server.sendmail(sender_address, receiver_address, message)
     
    # Close our endpoint
    smtp_server.close()



