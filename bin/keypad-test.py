# This example is a hello world example
# for using a keypad with the Raspberry Pi

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

L1 = 5
L2 = 6
L3 = 13
L4 = 19

C1 = 12
C2 = 16
C3 = 20
C4 = 21

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def readLine(line, characters, pwd):
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        pwd.append(characters[0])
    if(GPIO.input(C2) == 1):
        pwd.append(characters[1])
    if(GPIO.input(C3) == 1):
        pwd.append(characters[2])
    if(GPIO.input(C4) == 1):
        pwd.append(characters[3])
    GPIO.output(line, GPIO.LOW)
    
try:
    while True:
        PASSWORD = ['1','1','1','1']
        pwd = []
        while len(pwd) != 4:
            readLine(L1, ["1","2","3","A"], pwd)
            readLine(L2, ["4","5","6","B"], pwd)
            readLine(L3, ["7","8","9","C"], pwd)
            readLine(L4, ["*","0","#","D"], pwd)
            time.sleep(0.1)
        print(pwd)
        print(PASSWORD)
        for i in range(4):
            if pwd[i] == PASSWORD[i]:
                continue
                if pwd[3] == PASSWORD[3]:
                    print('Righ password.')
                    break
            else:
                print('Wrong password.')
                break
except KeyboardInterrupt:
    print("\nApplication stopped!")
