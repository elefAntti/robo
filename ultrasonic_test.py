#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep

button = Button()
client = obj_pipe.send(("localhost", 8001))
us = UltrasonicSensor() 
# Put the US sensor into distance mode.
us.mode='US-DIST-CM'

while not button.any():
    sleep(0.02)
    client.on_next(us.value() / 10)