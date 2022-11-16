import adafruit_dht
import board
import time

dht = adafruit_dht.DHT11(board.D2)
pin = 2

while True:
    try:
        temperature = dht.temperature
        humidity = dht.humidity
        print('Temperature: ', temperature, ' °C\nHumidity: ', humidity, ' %\n')
        time.sleep(2)
    except RuntimeError as error:
        print(error.args[0])
        raise error
    except Exception as error:
        dht.exit()
        raise error
    
