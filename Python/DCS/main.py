__author__ = 'Andry'

# coding: utf-8

import serial
import pywapi
from datetime import datetime, date, time
from time import sleep


print ("Программа мониторинга беспроводных датчиков RF_DCS")

found = False

for i in range(64) :
  try :
#    port = "COM%d" % i
    port = "/dev/ttyUSB%d" % i
    ser = serial.Serial(port)
    ser.close()
    print ("Найден последовательный порт: ", port)
    found = True
  except serial.serialutil.SerialException :
    pass
print ("Поиск завершен")

if not found :
  print ("Последовательных портов не обнаружено")

#ser = serial.Serial("COM3")
ser = serial.Serial("/dev/ttyUSB0")
ser.baudrate = 9600
print ("COM порт открыт")

#f_log = open('log.txt','a')
#f_t1 = open('t1.txt','a')
#f_t2 = open('t2.txt','a')
#f_t3 = open('t3.txt','a')
#f_t4 = open('t4.txt','a')

sensor1=''
sensor2=''
sensor3=''
sensor4=''

while True :
    line = ser.readline()
    str_to_file=line.decode('big5')
#   print (line)
#   print (str_to_file)
    now_time = datetime.now() # Текущая дата со временем
    log_str=now_time.strftime("%d.%m.%Y %H:%M:%S  ") + str_to_file  # форматируем дату
    print (log_str)
    f_log = open('log.txt','a')
    f_log.write(log_str)
    f_log.close()

#    print(str_to_file[3:9])
#    print(str_to_file[33:37])

    #sensor #1
    if str_to_file[3:9]=='0x1EE0' and str_to_file[33:37]=='tdeg' :
        f_t1 = open('t1.txt','a')
        f_t1.write(now_time.strftime("%d.%m.%Y%%%H:%M:%S%%") + str_to_file[38:41] + '\n')
        f_t1.close()
        sensor1=str_to_file[38:41]

    #sensor #2
    if str_to_file[3:9]=='0x2EE0' and str_to_file[33:37]=='tdeg' :
        f_t1 = open('t2.txt','a')
        f_t1.write(now_time.strftime("%d.%m.%Y%%%H:%M:%S%%") + str_to_file[38:41] + '\n')
        f_t1.close()
        sensor2=str_to_file[38:41]

    #sensor #3
    if str_to_file[3:9]=='0x3EE0' and str_to_file[33:37]=='tdeg' :
        f_t1 = open('t3.txt','a')
        f_t1.write(now_time.strftime("%d.%m.%Y%%%H:%M:%S%%") + str_to_file[38:41] + '\n')
        f_t1.close()
        sensor3=str_to_file[38:41]
        tempr_renew = True

    #sensor #4
    if str_to_file[3:9]=='0x4EE0' and str_to_file[33:37]=='tdeg' :
        f_t1 = open('t4.txt','a')
        f_t1.write(now_time.strftime("%d.%m.%Y%%%H:%M:%S%%") + str_to_file[38:41] + '\n')
        f_t1.close()
        sensor4=str_to_file[38:41]
    try:
        #outer temperature from weather.com
        weather_com_result = pywapi.get_weather_from_weather_com('UPXX2317')
        if 'error' in weather_com_result:
            print('Weather.com error: ' + weather_com_result['error'])
            raise RuntimeError('Weather error')
        now_time = datetime.now() # Текущая дата со временем
        print ("Weather.com says: It is " + weather_com_result['current_conditions']['text'].lower() + " and " + weather_com_result['current_conditions']['temperature'] + "C now in Kaniv.")
        f_tout = open('out_t.txt','a')
        f_tout.write(now_time.strftime("%d.%m.%Y%%%H:%M:%S%%") + weather_com_result['current_conditions']['temperature'] + '\n')
        f_tout.close()
#        sleep(60)
    except Exception as e:
        print(e)
        sleep(1)

    print( '\nПодача: ' + sensor4 + '\nОбратка: ' + sensor1 + '\nДверцята: ' + sensor3 + '\nКiмната: ' + sensor2 + '\n')
