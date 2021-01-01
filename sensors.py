import RPi.GPIO as GPIO
import time
import requests
import urllib3
from app3 import lights_now
import random
from datetime import datetime

GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.IN)

time.sleep(5)

while True:
    if GPIO.input(14) == True:
        now = datetime.now()
        now = now.strftime('%H:%M:%S')
        print(f'motion detected at {now}')

        hour = int(time.strftime("%H"))
        try:
            b, status, elec = lights_now()
            if elec == 'Power' and  6 > hour > 22:
                # bri = random.randint(1,100)
                b.lights[3].state(on= True, bri=170)
                time.sleep(15)
                b.lights[3].state(on= False)
        except requests.exceptions.ConnectionError or urllib3.exceptions.MaxRetryError:
            print('There is no power')

    time.sleep(1)