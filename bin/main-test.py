import RPi.GPIO as GPIO
import time
import board
# Import Adafruit_IO library and create instance of REST client.
from Adafruit_IO import RequestError, Client, Feed
import adafruit_mpu6050

# GPIO SETUP:
#   Mode: BCM
#   IO devices: GY-521, PIR HC-SR501, KY-036, LED, Active Buzzer

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# GY-521 input
i2c = board.I2C()  # uses board.SCL and board.SDA
mpu = adafruit_mpu6050.MPU6050(i2c)
# PIR HC-SR501 input
PIR_PIN = 14
GPIO.setup(14, GPIO.IN, GPIO.PUD_DOWN)
# KY-036 input
TOUCH_PIN = 27
GPIO.setup(TOUCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# LED output
LED_PIN = 15
GPIO.setup(15, GPIO.OUT)
# Active Buzzer output
BUZZER_PIN = 17
GPIO.setup(17, GPIO.OUT)

# Adafruit Client connection
ADAFRUIT_IO_USERNAME = 'compiotgroup3'
ADAFRUIT_IO_KEY = 'aio_gpXs67Bn7HYZmTFj0t1Zuisebnv5'

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Connecting/creating Adafruit IO feeds

# Smart Garage feed
try:
    smartgarage_feed = aio.feeds('smartgarage')
except RequestError:
    smartgarage_feed = Feed(name='smartgarage')
    smartgarage_feed = aio.create_feed(smartgarage_feed)
# Garage door feed
try:
    garage_feed = aio.feeds('garage')
except RequestError:
    garage_feed = Feed(name='garage')
    garage_feed = aio.create_feed(garage_feed)
# LED motion light feed
try:
    led_feed = aio.feeds('motion-light')
except RequestError:
    led_feed = Feed(name='motion-light')
    led_feed = aio.create_feed(led_feed)
# PIR motion sensor feed    
try:
    motion_feed = aio.feeds('hc-sr501')
except RequestError:
    motion_feed = Feed(name='hc-sr501')
    motion_feed = aio.create_feed(motion_feed)
# Alarm feed    
try:
    alarm_feed = aio.feeds('alarm-feed')
except RequestError:
    alarm_feed = Feed(name='alarm-feed')
    alarm_feed = aio.create_feed(alarm_feed)
# Temperature feed
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
    # Garage door (OPEN - 0, CLOSED - 1)
    garage_door = GPIO.input(TOUCH_PIN)

    txt_motion = ''
    # if no motion detected (input is 0)
    if motion == 0:
        message = 'No motion detected.'
        aio.send_data(led_feed.key, motion)
        aio.send_data(motion_feed.key, txt_motion)
        GPIO.output(LED_PIN,0)
        time.sleep(2)
        print(txt_motion)
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
            print(txt_motion)
        # else if alarm is off
        else:
            message = 'Motion detected.'
            GPIO.output(BUZZER_PIN,GPIO.LOW)
            print(txt_motion)

        aio.send_data(led_feed.key, motion)
        aio.send_data(motion_feed.key, txt_motion)
        
    aio.send_data(temperature_feed.key, temperature)
    time.sleep(2)
    # print("Temperature: %.2f C" % temperature)


