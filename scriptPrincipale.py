import time
import csv
from bme280 import BME280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

import logging

import datetime

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("""weather.py - Print readings from the BME280 weather sensor.

Press Ctrl+C to exit!

""")

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

name_datafile = 'data_' + datetime.datetime.now().strftime("%Y-%m-%dh%Hm%Ms%Sms%f") + '.txt'

datafile = open(name_datafile, "w")

field_names = ['Data;', 'Temperatura (°C);', 'Pressione (hPa);', 'Umidità (%);']
datafile.writelines(field_names)

temperature = bme280.get_temperature()
pressure = bme280.get_pressure()
humidity = bme280.get_humidity()
time.sleep(3)

while True:
    x = datetime.datetime.now()
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    logging.info("""\n Temperature: {:05.2f} *C \n Pressure: {:05.2f} hPa \n Relative humidity: {:05.2f} % """.format(temperature, pressure, humidity))
    datafile.write('\n')
    datafile.write(str(x)+';'+str(temperature)+';'+str(pressure)+';'+str(humidity))
    datafile.close()
    if(x.hour==8 and x.minute<15):
        secondiDelay=x.second+x.minute*60
        time.sleep(900-secondiDelay)
    else:
        time.sleep(900) #valore in secondi, 1800 per registrare i dati ogni 30 minuti
    datafile = open(name_datafile, "a")
