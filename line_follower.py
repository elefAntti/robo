#!/usr/bin/env python3

from ev3dev import ev3
from time import sleep
import socket
import sys

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
<<<<<<< HEAD
turn = 200
bright = 15
=======
turn = 20
bright = 60
>>>>>>> 8d9ef7a047e3a90d1514606a928a484068437bbc

def spin_around():
    lmotor = ev3.LargeMotor('outA')
    rmotor = ev3.LargeMotor('outB')
<<<<<<< HEAD
    lmotor.stop()
    rmotor.stop()

=======
>>>>>>> 8d9ef7a047e3a90d1514606a928a484068437bbc
    while not button.any():
        #ll = llight.value()
        #rl = rlight.value()
        #pos = ll-rl
        #print(ll, rl, pos)
        print(light.value())

<<<<<<< HEAD
        tspd = -120
=======
        tspd = -30
>>>>>>> 8d9ef7a047e3a90d1514606a928a484068437bbc
        rspd = 0

        #if (pos > bigDiff):
        #    rspd = -bigTurn
        #elif (pos > lilDiff):
        #    rspd = -lilTurn
        #if (pos < -bigDiff):
        #    rspd = bigTurn
        #elif (pos < -lilDiff):
        #    rspd = lilTurn
        if light.value() > bright:
<<<<<<< HEAD
            rspd = -turn
        else:
            rspd = turn

        right = (tspd+rspd)/2.0
        left = tspd-right
        print(left, right)
        
        lmotor.run_forever(speed_sp=left)
        rmotor.run_forever(speed_sp=right)
    lmotor.stop()
    rmotor.stop()

for i in range(5):
    print("Following a line")
spin_around()
=======
            rspd = turn
        else:
            rspd = -turn

        right = (tspd+rspd)/2.0
        left = tspd-right
        
        lmotor.run_forever(speed_sp=left)
        rmotor.run_forever(speed_sp=right)

for i in range(5):
    print("Following a line")
spin_around()
>>>>>>> 8d9ef7a047e3a90d1514606a928a484068437bbc
