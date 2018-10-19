#!/usr/bin/env python3

from ev3dev import ev3
from time import sleep
import socket
import sys
from lib import RemoteControlSocket, RobotInterface

forwardSpeed = 360

#ip = '169.254.130.192'
ip = ''

motorA = ev3.LargeMotor('outA')
motorB = ev3.LargeMotor('outB')
robot = RobotInterface.RobotInterface('outA','outB')
motorC = ev3.MediumMotor('outC')
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
        robot.simpleDrive(
            forwardSpeed * int(motorSpeeds[0]),
            forwardSpeed * int(motorSpeeds[1]))
        motorC.run_forever(speed_sp = forwardSpeed * int(motorSpeeds[2]))
    else:
        robot.simpleDrive(forwardSpeed, forwardSpeed)

motorC.stop()

