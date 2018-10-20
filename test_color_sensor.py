#!/usr/bin/env python3

from ev3dev import ev3
import time
import socket
import sys

#ip = '169.254.130.192'
ip = ''

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (ip, 8000)

sock.bind(server_address)

light = ev3.ColorSensor()
button = ev3.Button()

while not button.any():
    print('give me command')
    d, server = sock.recvfrom(64)
    print('doing {} for {} seconds')
    startTime = time.time()
    d = d.decode("utf-8")
    arr = d.split()
    data = arr[0]
    timeout = arr[1]
    print('doing {} for {} seconds'.format(data, timeout))
    if data == 'r':
        light.mode = 'COL-REFLECT'
    elif data == 'a':
        light.mode = 'COL-AMBIENT'
    elif data == 'x':
        light.mode = 'RGB-RAW'
    elif data == 'c':
        light.mode = 'COL-COLOR'
    elif data == 'z':
        print('bye bye')
        break
    while time.time() - startTime < float(timeout):
        if data == 'x':
            print(light.value(0), light.value(1), light.value(2))
            #yellow is 0: 85-100, 1: 40-50, 2: 0-10
        elif data == 'c':
            colors=('unknown','black','blue','green','yellow','red','white','brown')
            print(colors[light.value()])
        else:
            print(light.value())
