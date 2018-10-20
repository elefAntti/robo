#!/usr/bin/env python3

from ev3dev import ev3
from time import sleep
import socket
import sys
from lib import RemoteControlSocket, RobotInterface

forwardSpeed = 360

robot = RobotInterface.RobotInterface('outA','outB')
#motorC = ev3.MediumMotor('outC')
button = ev3.Button()

print("Motors connected.")

remote = RemoteControlSocket.RemoteControlSocket()

print("Socket set.")

print("Connected")
manual = True

while not button.any():

    ##if data == "manual":
    ##    manual = True
    ##    print("Switching to manual controls.")
    ##elif data == "release":
    ##    print("Continuing independent execution.")
    ##    manual = False

    if manual:
        motorSpeeds = remote.receive()
        robot.simpleDrive(motorSpeeds[0], motorSpeeds[1])
        #robot.logStuff()
        #motorC.run_forever(speed_sp = forwardSpeed * int(motorSpeeds[2]))
    else:
        robot.simpleDrive(forwardSpeed, forwardSpeed)

robot.stop()
#motorC.stop()

