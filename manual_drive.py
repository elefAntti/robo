#!/usr/bin/env python3

from ev3dev import ev3
from time import sleep
import socket
import sys

#ip = '169.254.130.192'
ip = ''
forwardSpeed = 360
turnBigSpeed = 180
turnSmallSpeed = -180

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (ip, 8000)

sock.bind(server_address)

motorA = ev3.LargeMotor('outA')
motorB = ev3.LargeMotor('outB')
motorC = ev3.MediumMotor('outC')
button = ev3.Button()

print("Connected")

while not button.any():
    data, server = sock.recvfrom(64)
    data = data.decode("utf-8")
    motorSpeeds = data.split[',']
    if len(motorSpeeds) == 3 and
        motorSpeeds[0].isdigit() and
        motorSpeeds[1].isdigit() and
        motorSpeeds[2].isdigit():
        motorA.run_forever(speed_sp = forwardSpeed * int(motorSpeeds[0]))
        motorB.run_forever(speed_sp = forwardSpeed * int(motorSpeeds[1]))
        motorC.run_forever(speed_sp = forwardSpeed * int(motorSpeeds[2]))

motorA.stop()
motorB.stop()
motorC.stop()
