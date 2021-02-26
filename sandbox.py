# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 15:28:10 2021

@author: Computer
"""

import TradingFunctions as tf


alert = True

if True:
            
    DKNG_Price_String = tf.get_live_price('DKNG')
    DKNG_Price_Float = float(tf.get_live_price('DKNG'))
       
    if(DKNG_Price_Float > 55.00):
        volume = tf.get_volume('DKNG')
        tenDayVolume = tf.get_10_day_average_volume('DKNG')
        
        moreless = 'higher'
        percent = round(((volume/tenDayVolume)*100-100),2)
        
        if volume < tenDayVolume:
            moreless = 'lower'
            percent = round((100-(volume/tenDayVolume)*100),2)
            
            
        message1 = 'DKNG stock price is now at $' + str(DKNG_Price_String) + '.'
        message2 = 'The volume currently traded is ' + str(percent) + '% ' + moreless + ' than the 10 day average.' 
        
        print(message1)
        print(message2)
        
        #send_email_to_joe(message1,message2)
        alert = False            
        
    else:
        print('DKNG stock price is now at $' + str(DKNG_Price_String) + '.')
        
else:
    print('market closed')
    
#time.sleep(600)