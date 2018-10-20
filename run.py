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

robot = RobotInterface.RobotInterface('outB','outA', flip_dir = True)
button = ev3.Button()

print("Motors connected.")

remote = RemoteControlSocket.RemoteControlSocket()

print("Socket set.")

environment = { "robot": robot }

fsm = Statemachine(environment)

print("Connected")
manual = True
hack = False
operation = None

while not button.any():
    motorSpeeds, state = remote.receive()
    if state == 0:
        manual = True
        hack = False
    elif state == 666:
        if not hack:
            print("Entering %d"%state) 
            hack = True
            operation = RobotInterface.GyroPivot(robot, 90)
        ready = operation.update()
        if ready: 
            manual = True
    else:
        if manual:
            fsm.SetState(States(state))
            print("Entering %d"%state) 
        manual = False

    if manual and not hack:
        robot.simpleDrive(motorSpeeds[0], motorSpeeds[1])
    else:
        fsm.Run()

robot.stop()


