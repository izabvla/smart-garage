import Adafruit_DHT
import time

DHT_SENSOR = adafruit_dht.DHT11
DHT_PIN = 2

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print('Temp = {0:0.1f}C Humidity = {1:0.1f}%'.format(temperature, humidity))
    else:
        print('Sensor failure. Trying again...')
    time.sleep(3)
    
'''
import board
import psutil

for proc in psutil.process_iter():
   if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
       proc.kill()

sensor = Adafruit_DHT.DHT11(board.D2)

while True:
    try:
        temp = sensor.temperature
        humidity = sensor.humidity
        print('Temperature: {}*C    Humidity: {}%'.format(temp,humidity))
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2)
        continue
    except Exception as error:
        sensor.exit()
        raise error
        
    time.sleep(2)
'''
