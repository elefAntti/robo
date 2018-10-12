#!/usr/bin/env python3

from ev3dev import ev3
from time import sleep
import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('169.254.45.0', 8000)

sock.bind(server_address)

motor = ev3.LargeMotor('outB')
button = ev3.Button()

print("Hello world")

data, server = sock.recvfrom(6)

motor.run_forever(speed_sp = 360)

while button.any():
    sleep(0.11)


while not button.any():
    sleep(0.11)

motor.stop()