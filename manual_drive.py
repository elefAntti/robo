#!/usr/bin/env python3

from ev3dev import ev3
from time import sleep
import socket
import sys

ip = '169.254.130.192'
forwardSpeed = 360
turnBigSpeed = 180
turnSmallSpeed = -180

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (ip, 8000)

sock.bind(server_address)

#motorA = ev3.LargeMotor('outA')
#motorB = ev3.LargeMotor('outB')
button = ev3.Button()

print("Connected")

while not button.any():
    data, server = sock.recvfrom(64)
    if data == 'forw':
        print('forw')
        #motorA.run_forever(speed_sp = forwardSpeed)
        #motorB.run_forever(speed_sp = forwardSpeed)
    elif data == 'back':
        print('back')
        #motorA.run_forever(speed_sp = -forwardSpeed)
        #motorB.run_forever(speed_sp = -forwardSpeed)
    elif data == 'left':
        print('left')
        #motorA.run_forever(speed_sp = turnBigSpeed)
        #motorB.run_forever(speed_sp = turnSmallSpeed)
    elif data == 'right':
        print('right')
        #motorA.run_forever(speed_sp = turnSmallSpeed)
        #motorB.run_forever(speed_sp = turnBigSpeed)
    else:
        print('halt')
        #motorA.stop()
        #motorB.stop()

#motorA.stop()
#motorB.stop()
