# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 20:02:16 2021

@author: Compute
"""

import TradingFunctions as tf



symbols = tf.update_symbols()
volume = []
price = []

average_volume = []
average_10_day_volume = []


for sym in symbols:
    price.append(tf.get_live_price(sym))
    
    volume.append(tf.get_average_volume(sym))
    average_volume.append(tf.get_average_volume(sym))
    average_10_day_volume.append(tf.get_10_day_average_volume(sym))
    
    
'''  

i = 0
for vol in volume:
    print(symbols[i] + " " + str(vol) + " " + str(price[i]))
    i = i + 1
    
    '''
    
    

    
    
#for i in range(25):  
#    send_email_to_joe("this is a test","a very dumb test")














"""
response = create_order("MSFT",10,"sell","market","gtc")

print(response['symbol'] + ' ' + response['qty'])

orders = get_orders()


for i in range(10):
    print(orders[i]['symbol'])
    
 """   





    

#get_volume("MSFT")


#get_regular_market_price('MSFT')