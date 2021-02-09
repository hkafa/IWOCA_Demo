import smbus
import time
from pandas import DataFrame
from datetime import datetime
from app import *

def sensor_read ():
    DEVICE_BUS = 1
    DEVICE_ADDR = 0x17

    TEMP_REG = 0x01
    LIGHT_REG_L = 0x02
    LIGHT_REG_H = 0x03
    STATUS_REG = 0x04
    ON_BOARD_TEMP_REG = 0x05
    ON_BOARD_HUMIDITY_REG = 0x06
    ON_BOARD_SENSOR_ERROR = 0x07
    BMP280_TEMP_REG = 0x08
    BMP280_PRESSURE_REG_L = 0x09
    BMP280_PRESSURE_REG_M = 0x0A
    BMP280_PRESSURE_REG_H = 0x0B
    BMP280_STATUS = 0x0C
    HUMAN_DETECT = 0x0D

    bus = smbus.SMBus(DEVICE_BUS)

    aReceiveBuf = []

    aReceiveBuf.append(0x00)

    for i in range(TEMP_REG,HUMAN_DETECT + 1):
        aReceiveBuf.append(bus.read_byte_data(DEVICE_ADDR, i))
    sensor_readings = {}
    #motion detection
    sensor_readings['motion'] = True if aReceiveBuf[HUMAN_DETECT] == 1 else False

    #Light intensity
    if aReceiveBuf[STATUS_REG] & 0x04 :
        sensor_readings['lux'] = 0
    elif aReceiveBuf[STATUS_REG] & 0x08 :
        sensor_readings['lux'] = 0
    else :
        sensor_readings['lux'] = (aReceiveBuf[LIGHT_REG_H] << 8 | aReceiveBuf[LIGHT_REG_L])

    #Temperature off-board
    if aReceiveBuf[STATUS_REG] & 0x01 :
        sensor_readings['ambient_temp'] = 'Over range'
    elif aReceiveBuf[STATUS_REG] & 0x02 :
        sensor_readings['ambient_temp'] = 'sensor not connected'
    else :
        sensor_readings['ambient_temp'] = aReceiveBuf[TEMP_REG]

    #Temperature on-board
    sensor_readings['on_board_temp'] = aReceiveBuf[ON_BOARD_TEMP_REG]

    #humidity
    sensor_readings['humidity'] = aReceiveBuf[ON_BOARD_HUMIDITY_REG]

    #Pressure
    sensor_readings['pressure'] = aReceiveBuf[BMP280_PRESSURE_REG_L] | aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | aReceiveBuf[BMP280_PRESSURE_REG_H] << 16

    return sensor_readings

if __name__ == '__main__':

    pressure_data = []
    counter = 0

    while True:
        readings = sensor_read()
        p1 = Sensors_db(pressure=readings['pressure'])
        db.session.add(p1)
        db.session.commit()
        print(counter)
        time.sleep(10)
        counter += 1
