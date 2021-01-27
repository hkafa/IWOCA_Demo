import RPi.GPIO as GPIO
import time
from app import lights_now
from hub import sensor_read

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
time.sleep(1)


def timer():
    t = 0
    time.sleep(1)
    t +=1
    return t

current_time = time.strftime("%H", time.localtime())

while True:
    b, status, elec = lights_now()
    readings = sensor_read()
    t = time.localtime()
    hour = int(time.strftime("%H", t)) + 2
    print(hour)
    print(readings['lux'])
    if elec == 'No Power' and readings['lux'] < 120 and (hour >= 15 or hour < 4):
        GPIO.output(4, GPIO.HIGH)
        time.sleep(1)
        # if readings['motion'] == False and :
        #     elapsed_time = time.time() - start_time
        #     start_time = time.time()
        #     time.sleep(10)
        #     elapsed_time = time.time() - start_time
        #     elapsed_time
    else:
        GPIO.output(4, GPIO.LOW)
        time.sleep(1)

