import RPi.GPIO as GPIO
import time
import sys
import signal
import requests

GPIO.setmode(GPIO.BCM)

STALLNUMS = [0,1]

DOOR_SENSOR_0 = 18
DOOR_SENSOR_1 = 12
SENSE = [DOOR_SENSOR_0, DOOR_SENSOR_1]

isOpen0 = None
oldIsOpen0 = None
isOpen1 = None
oldIsOpen1 = None

curr = [isOpen0, isOpen1]
old = [oldIsOpen0, oldIsOpen1]

GPIO.setup(DOOR_SENSOR_0, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(DOOR_SENSOR_1, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def update(num):
    old[num] = curr[num]
    curr[num] = GPIO.input(SENSE[num])
    if (curr[num] and (curr[num] != old[num])):
        print "Unoccupied " + str(num)
    elif (curr[num] != old[num]):
        print "Occupied " + str(num) 
    try:
        r = requests.put("http://when2poop.ga/api/stalls/"+str(STALLNUMS[num])+"?avail="+("1" if curr[num] else "-1"))
    except requests.exceptions.RequestException as e:
        print e
        sleep(30)


while True:
    update(0)
    update(1)
    time.sleep(5)
