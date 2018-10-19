#!/usr/bin/env python3

from ev3dev import ev3
from time import sleep
import socket
import sys

<<<<<<< 10f5043815b3e0c46952e9fb45c5963b47f5840b
#llight_port = 1
#rlight_port = 2

#llight = ev3.ColorSensor(port=llight_port)
#rlight = ev3.ColorSensor(port=rlight_port)
light = ev3.ColorSensor()
button = ev3.Button()
#llight.mode = 'COL-REFLECT'
#rlight.mode = 'COL-REFLECT'
light.mode = 'COL-REFLECT'

#bigTurn = 40
#lilTurn = 20
#bigDiff = 130
#lilDiff = 60
turn = 20
bright = 60
=======
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
>>>>>>> untested code from prev year

def spin_around():
    lmotor = ev3.LargeMotor('outA')
    rmotor = ev3.LargeMotor('outB')
<<<<<<< 10f5043815b3e0c46952e9fb45c5963b47f5840b
    while not button.any():
        #ll = llight.value()
        #rl = rlight.value()
        #pos = ll-rl
        #print(ll, rl, pos)
        print(light.value())
=======
    while True:
        ll = llight.value()
        rl = rlight.value()
        pos = ll-rl
        print(ll, rl, pos)
>>>>>>> untested code from prev year

        tspd = -30
        rspd = 0

<<<<<<< 10f5043815b3e0c46952e9fb45c5963b47f5840b
        #if (pos > bigDiff):
        #    rspd = -bigTurn
        #elif (pos > lilDiff):
        #    rspd = -lilTurn
        #if (pos < -bigDiff):
        #    rspd = bigTurn
        #elif (pos < -lilDiff):
        #    rspd = lilTurn
        if light.value() > bright:
            rspd = turn
        else:
            rspd = -turn
=======
        if (pos > bigDiff):
            rspd = -bigTurn
        elif (pos > lilDiff):
            rspd = -lilTurn
        if (pos < -bigDiff):
            rspd = bigTurn
        elif (pos < -lilDiff):
            rspd = lilTurn
>>>>>>> untested code from prev year

        right = (tspd+rspd)/2.0
        left = tspd-right
        
        lmotor.run_forever(speed_sp=left)
        rmotor.run_forever(speed_sp=right)

for i in range(5):
    print("Following a line")
spin_around()