# modularize
# (rewrite every process as functions, write main function)

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
# BOARD -> Standard pin board numbering
# 1 2
# 3 4
# 5 6
# ...

# PIR input, LED output
GPIO.setup(11, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(3, GPIO.OUT)

# Import Adafruit_IO library and create instance of REST client.

from Adafruit_IO import RequestError, Client, Feed

ADAFRUIT_IO_USERNAME = 'compiotgroup3'
ADAFRUIT_IO_KEY = 'aio_gpXs67Bn7HYZmTFj0t1Zuisebnv5'

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# connecting/creating adafruit feeds
try:
    led_feed = aio.feeds('motion-light')
except RequestError: # Doesn't exist, create new feed
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

#receiving and sending data
while True:
    motion = GPIO.input(11)
    # debug: alarm never == 1 ?
    alarm = aio.receive('alarm-feed').value
    
    # if no motion detected (input is 0)
    if motion == 0:
        print('No motion', motion)
        aio.send_data(led_feed.key, motion)
        aio.send_data(motion_feed.key, 'No motion detected.')
        GPIO.output(3,0)
        time.sleep(2)
    # if motion detected and alarm is on (input is 1)
    elif motion == 1 and alarm == 1:
        GPIO.output(3,1)
        print('Intruder alert - alarm: ', alarm.value)
        aio.send_data(led_feed.key, motion)
        aio.send_data(motion_feed.key, 'Motion detected. Alarm engaged, possible intruder alert.')
        time.sleep(2)
    # if motion detected and alarm is off (1 and 0)
    else:
        GPIO.output(3,1)
        print('Motion detected - motion: ', motion)
        aio.send_data(led_feed.key, motion)
        aio.send_data(motion_feed.key, 'Motion detected.')
        time.sleep(2)





