import RPi.GPIO as GPIO
import time
import requests
import urllib3
from app import lights_now
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

        now = datetime.now()
        hour = int(now.strftime("%H"))
        print(f'{hour}')
        try:
            b, status, elec = lights_now()
            if elec == 'Power' and (hour > 20 or hour < 4):
                # bri = random.randint(1,100)
                print('conditions met')
                b.lights[3].state(on= True, bri=25)
                time.sleep(15)
                b.lights[3].state(on= False)
        except requests.exceptions.ConnectionError or urllib3.exceptions.MaxRetryError:
            print('There is no power')

    time.sleep(1)