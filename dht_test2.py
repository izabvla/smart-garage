import Adafruit_DHT
import time
import board
import psutil

for proc in psutil.process_iter():
   if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
       proc.kill()

sensor = Adafruit_DHT.DHT11(board.D4)

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
