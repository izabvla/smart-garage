import RPi.GPIO as GPIO
import time
import board
import adafruit_mpu6050

# GY-521
i2c = board.I2C()  # uses board.SCL and board.SDA
mpu = adafruit_mpu6050.MPU6050(i2c)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# PIR input
GPIO.setup(14, GPIO.IN, GPIO.PUD_DOWN)
PIR_PIN = 14
# LED output
GPIO.setup(15, GPIO.OUT)
LED_PIN = 15
# Buzzer output
GPIO.setup(17, GPIO.OUT)
BUZZER_PIN = 17

# Import Adafruit_IO library and create instance of REST client.
from Adafruit_IO import RequestError, Client, Feed

ADAFRUIT_IO_USERNAME = 'compiotgroup3'
ADAFRUIT_IO_KEY = 'aio_gpXs67Bn7HYZmTFj0t1Zuisebnv5'

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# connecting/creating adafruit feeds
try:
    led_feed = aio.feeds('motion-light')
except RequestError:
    led_feed = Feed(name='motion-light')
    led_feed = aio.create_feed(led_feed)
    
try:
    motion_feed = aio.feeds('hc-sr501')
except RequestError:
    motion_feed = Feed(name='hc-sr501')
    motion_feed = aio.create_feed(motion_feed)
    
try:
    alarm_feed = aio.feeds('alarm-feed')
except RequestError:
    alarm_feed = Feed(name='alarm-feed')
    alarm_feed = aio.create_feed(alarm_feed)

try:
    temperature_feed = aio.feeds('temperature')
except RequestError:
    temperature_feed = Feed(name='temperature')
    temperature_feed = aio.create_feed(temperature_feed)

#receiving and sending data
while True:
    # Motion status (ON -1, OFF - 0)
    motion = GPIO.input(PIR_PIN)
    # Alarm status (ON -1, OFF - 0)
    alarm_status = aio.receive('alarm-feed').value
    # Temperature
    temperature = mpu.temperature
    
    #
    message = ''
    
    # if no motion detected (input is 0)
    if motion == 0:
        message = 'No motion detected.'
        aio.send_data(led_feed.key, motion)
        aio.send_data(motion_feed.key, message)
        GPIO.output(LED_PIN,0)
        time.sleep(2)
        print(message)
    # if motion detected
    else:
        # LED ON
        GPIO.output(LED_PIN,1)
        # if alarm is on
        if alarm_status == '1':
            message = 'Motion detected. Intruder alert.'
            GPIO.output(BUZZER_PIN,GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            print(message)
        # else if alarm is off
        else:
            message = 'Motion detected.'
            GPIO.output(BUZZER_PIN,GPIO.LOW)
            print(message)

        aio.send_data(led_feed.key, motion)
        aio.send_data(motion_feed.key, message)
        
    aio.send_data(temperature_feed.key, temperature)
    time.sleep(2)
    # print("Temperature: %.2f C" % temperature)


