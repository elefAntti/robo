#!/usr/bin/env python3

from ev3dev import ev3
from time import sleep
import socket
import sys

forwardSpeed = 360

#ip = '169.254.130.192'
ip = ''

motorA = ev3.LargeMotor('outA')
motorB = ev3.LargeMotor('outB')
motorC = ev3.MediumMotor('outC')
button = ev3.Button()

print("Motors connected.")

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (ip, 8000)

sock.bind(server_address)

print("Socket set.")

print("Connected")

while not button.any():
    manual = False
    data, server = sock.recvfrom(64)
    data = data.decode("utf-8")
    print("Received", data)

    if data == "manual":
        manual = True
        print("Switching to manual controls.")
    elif data == "release":
        print("Continuing independent execution.")
        manual = False

    if manual:
        motorSpeeds = data.split[',']
        if len(motorSpeeds) == 3 and \
            motorSpeeds[0].isdigit() and \
            motorSpeeds[1].isdigit() and \
            motorSpeeds[2].isdigit():
            motorA.run_forever(speed_sp = forwardSpeed * int(motorSpeeds[0]))
            motorB.run_forever(speed_sp = forwardSpeed * int(motorSpeeds[1]))
            motorC.run_forever(speed_sp = forwardSpeed * int(motorSpeeds[2]))
    else:
        #aja muuta koodia
        motorA.run_forever(speed_sp = forwardSpeed)
        motorB.run_forever(speed_sp = forwardSpeed)
motorA.stop()
motorB.stop()
motorC.stop()

