#!/usr/bin/env python3

from ev3dev import ev3
from time import sleep
import socket
import sys

llight_port = 1
rlight_port = 2

llight = ev3.ColorSensor(port=llight_port)
rlight = ev3.ColorSensor(port=rlight_port)
llight.mode = 'COL-REFLECT'
rlight.mode = 'COL-REFLECT'

bigTurn = 40
lilTurn = 20
bigDiff = 130
lilDiff = 60

def spin_around():
    lmotor = ev3.LargeMotor('outA')
    rmotor = ev3.LargeMotor('outB')
    while True:
        ll = llight.value()
        rl = rlight.value()
        pos = ll-rl
        print(ll, rl, pos)

        tspd = -30
        rspd = 0

        if (pos > bigDiff):
            rspd = -bigTurn
        elif (pos > lilDiff):
            rspd = -lilTurn
        if (pos < -bigDiff):
            rspd = bigTurn
        elif (pos < -lilDiff):
            rspd = lilTurn

        right = (tspd+rspd)/2.0
        left = tspd-right
        
        lmotor.run_forever(speed_sp=left)
        rmotor.run_forever(speed_sp=right)

for i in range(5):
    print("Following a line")
spin_around()