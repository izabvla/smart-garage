# main.py

import RPi.GPIO as GPIO
import time
import keyboard

GPIO.setwarnings(False)
# GPIO.BOARD ->
#   1 2
#   3 4
#   5 ...
GPIO.setmode(GPIO.BOARD)

# PIR input, pin 8
GPIO.setup(8, GPIO.IN, GPIO.PUD_DOWN)
# LED output, pin 10
GPIO.setup(10, GPIO.OUT)
# Buzzer alarm output, pin 11
GPIO.setup(11, GPIO.OUT)

# Import Adafruit_IO library and create instance of REST client.
from Adafruit_IO import RequestError, Client, Feed

ADAFRUIT_IO_USERNAME = 'compiotgroup3'
ADAFRUIT_IO_KEY = 'aio_gpXs67Bn7HYZmTFj0t1Zuisebnv5'

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Establishing connection to Adafruit feeds
# Motion LED
try:
    ledFeed = aio.feeds('motion-light')
except RequestError: # Doesn't exist, create new feed
    led_feed = Feed(name='motion-light')
    led_feed = aio.create_feed(led_feed)
# PIR HC-SR501 Motion sensor
try:
    motion_feed = aio.feeds('hc-sr501')
except RequestError:
    motion_feed = Feed(name='hc-sr501')
    motion_feed = aio.create_feed(motion_feed)
# Buzzer alarm sensor
try:
    alarm_feed = aio.feeds('alarm-feed')
except RequestError:
    alarm_feed = Feed(name='alarm-feed')
    alarm_feed = aio.create_feed(alarm_feed)

def motion_detected():
    # motion: 1 - motion detected, 0 - no motion
    motion = GPIO.input(8)
    return True if motion == 1 else False

def alarm_activated():
    # alarm: 1 - alarm on, 0 - alarm off
    alarm = aio.receive('alarm-feed').value
    return True if alarm == 1 else False


def main():

    print('Smart Garage system is online. Press any key to start.')
    usr_in = input(':::')

    # While user input is not [Q] - Quit
    while usr_in.lower() is not 'q':
            
        # If any keyboard input -> press any key to resume, or Q to terminate
        if keyboard.is_pressed():
            print('Press any key to start, or [Q] - Quit')
            usr_in = input(':::')
            if usr_in.lower() is 'q':
                print('Smart Garage system is going offline.')
                break
        
        _motion = motion_detected()
        _alarm = alarm_activated()
        message = ""
        if _motion:
            if _alarm:
                # Turn on motion light and buzzer alarm
                GPIO.output(10,1)
                GPIO.output(11,GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(11, GPIO.LOW)
                message = 'Motion detected. Intruder alert.'
            # Turn on motion light and buzzer alarm
            GPIO.output(10,1)
            message = 'Motion detected.'
        else:
            message = 'No motion detected.'
        print(message)

        # Send data to Adafruit dashboards
        aio.send_data(led_feed.key, _motion)
        aio.send_data(motion_feed.key, message)

if __name__ == "__main__":
    main()