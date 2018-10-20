#!/usr/bin/env python3

from ev3dev import ev3
from time import sleep
import socket
import sys
from lib import RemoteControlSocket, RobotInterface
from lib.state import States
from statemachine import Statemachine

forwardSpeed = 360
print("Initializing")

robot = RobotInterface.RobotInterface('outA','outB')
button = ev3.Button()

print("Motors connected.")

remote = RemoteControlSocket.RemoteControlSocket()

print("Socket set.")

environment = { "robot": robot }

fsm = Statemachine(environment)

print("Connected")
manual = True

while not button.any():
    motorSpeeds, state = remote.receive()
    if state == 0:
        if manual:
            fsm.SetState(States(state)) 
        manual = True
    else:
        manual = False

    if manual:
        robot.simpleDrive(motorSpeeds[0], motorSpeeds[1])
    else:
        fsm.Run()

robot.stop()


