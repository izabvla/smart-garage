from RPi import GPIO
from time import sleep

TOUCH_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(TOUCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if GPIO.input(TOUCH_PIN) == GPIO.LOW:
        print("Garage door open")
    else:
        print("Garage door closed")
    sleep(4)

