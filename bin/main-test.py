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
# Heater feed
try:
    heater_feed = aio.feeds('heater')
except RequestError:
    heater_feed = Feed(name='heater')
    heater_feed = aio.create_feed(heater_feed)
# Fan feed
try:
    fan_feed = aio.feeds('fan')
except RequestError:
    fan_feed = Feed(name='fan')
    fan_feed = aio.create_feed(fan_feed)

# Receiving and sending data between Adafruit IO dashboard and sensors
while True:
    # Motion status (ON - 1, OFF - 0)
    motion = GPIO.input(PIR_PIN)
    # Alarm status (ON - 1, OFF - 0)
    alarm_status = aio.receive('alarm-feed').value
    # Temperature
    temperature = mpu.temperature
    # Heater & Fan status (ON - 1, OFF - 0)
    #heater_status = aio.receive('heater').value
    #fan_status = aio.receive('fan').value
    # Garage door (OPEN - 0, CLOSED - 1)
    garage_door = GPIO.input(TOUCH_PIN)

    # TEMPERATURE SYSTEM
    aio.send_data(temperature_feed.key, temperature)
    #if temperature > 35:
        # turn on fan
        #aio.send_data(fan_feed, 1)
        #aio.send_data(heater_feed, 0)
    #elif temperature < 5:
        # turn on heater
        #aio.send_data(fan_feed, 0)
        #aio.send_data(heater_feed, 1)
    #else:
        # do nothing
        #aio.send_data(fan_feed, 0)
        #aio.send_data(heater_feed, 0)

    # GARAGE DOOR SYSTEM
    if garage_door == GPIO.LOW:
        aio.send_data(garage_feed.key, 0)
        txt_door = 'Garage door open.'
    else:
        aio.send_data(garage_feed.key, 1)
        txt_door = 'Garage door closed.'
        
    # MOTION LIGHT & ALARM SYSTEM

    txt_motion = ''
    # If no motion detected (input is 0)
    if motion == 0:
        # LED motion light is turned off
        GPIO.output(LED_PIN, 0)
        txt_motion = 'No motion detected.'
        aio.send_data(led_feed.key, motion)
        aio.send_data(motion_feed.key, txt_motion)
    # if motion detected
    else:
        # LED motion light is turned on
        GPIO.output(LED_PIN,1)
        # If Alarm is on
        if alarm_status == '1':
            # Turn on buzzer
            GPIO.output(BUZZER_PIN,GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            txt_motion = 'Motion detected. Intruder alert.'
        # else if alarm is off
        else:
            # Make sure buzzer is off
            GPIO.output(BUZZER_PIN,GPIO.LOW)
            txt_motion = 'Motion detected.'

        aio.send_data(led_feed.key, motion)
        aio.send_data(motion_feed.key, txt_motion)
    

    # SMART GARAGE TEXT
    
    if temperature > 35:
        txt_temp = 'Temperature is too high, turn on fan if not already on.'
    elif temperature < 5:
        txt_temp = 'Temperature is too low, turn on heater if not already on.'
    else:
        txt_temp = 'Temperature is according to standards.'
    txt_smartgarage = '''Welcome to your Smart Garage.
    \n''' + txt_temp + '''\n''' + txt_motion + '''\n''' + txt_door + '''\n'''
    aio.send_data(smartgarage_feed.key, txt_smartgarage)

    print('\nLAST UPDATED: ' + time.ctime())
    print('\nTEMPERATURE: ' + temperature)
    print('\nMOTION/ALARM: ' + txt_motion)
    print('\nLIGHT: (ON - 1, OFF - 0)' + motion)
    print('\nGARAGE DOOR: (OPEN - 0, CLOSED - 1)' + garage_door)
    
    time.sleep(2)
