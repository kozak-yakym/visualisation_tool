__author__ = 'Andry'

# coding: utf-8

import pywapi
from datetime import datetime, date, time
from time import sleep

#weather_com_result = pywapi.get_weather_from_weather_com('UPXX2317')
#yahoo_result = pywapi.get_weather_from_yahoo('10001')
#noaa_result = pywapi.get_weather_from_noaa('KJFK')

#print ("Weather.com says: It is " + weather_com_result['current_conditions']['text'].lower() + " and " + weather_com_result['current_conditions']['temperature'] + "C now in Kaniv.")
#print("Yahoo says: It is " + yahoo_result['condition']['text'].lower() + " and " + yahoo_result['condition']['temp'] + "C now in New York.")
#print("NOAA says: It is " + noaa_result['weather'].lower() + " and " + noaa_result['temp_c'] + "C now in New York.")

print('Started')
while True :
    try:
        # Outer temperature from weather.com
        # TODO: move magic number UPXX2317 to the city code macro or constant.
        weather_com_result = pywapi.get_weather_from_weather_com('UPXX2317')
        if 'error' in weather_com_result:
            print('Weather.com error: ' + weather_com_result['error'])
            raise RuntimeError('Weather error')
        now_time = datetime.now() # Current time and date.
        print (now_time.strftime("%d/%m/%Y %H:%M:%S ") + "Weather.com says: It is " + weather_com_result['current_conditions']['text'].lower() + " and " + weather_com_result['current_conditions']['temperature'] + "C now in Kaniv.")
        f_tout = open('out_t.txt','a')
        f_tout.write(now_time.strftime("%d/%m/%Y%%%H:%M:%S%%") + weather_com_result['current_conditions']['temperature'] + '\n')
        f_tout.close()
        sleep(60)
    except Exception as e:
        print(e)
        sleep(1)
