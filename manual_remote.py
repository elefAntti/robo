import socket
import sys
import keyboard
pressedKeys = []
manual = False
release = False

ip = '192.168.43.21'

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = (ip, 8000)

def keyEvent(ke):
    leftMotorSpeed = 0
    rightMotorSpeed = 0
    handMotorSpeed = 0
    key = ke.name
    typ = ke.event_type
    manual = False
    release = False
    if typ == 'down':
        if key == 'm':
            manual = True
        elif key == 'n':
            release = True
        elif key not in pressedKeys:
            pressedKeys.append(key)
    if typ == 'up':
        if key == 'm':
            manual = False
        elif key == 'n':
            release = False
        elif key in pressedKeys:
            pressedKeys.remove(key)

    
    if manual:
        sock.sendto(bytes("manual", "UTF-8"), address)
        print("Manual override requested.")
        return
    if release:
        sock.sendto(bytes("release", "UTF-8"), address)
        print("Robot release requested.")
        return
    if 'w' in pressedKeys and 's' not in pressedKeys:
        leftMotorSpeed += 100
        rightMotorSpeed += 100
    if 's' in pressedKeys and 'w' not in pressedKeys:
        leftMotorSpeed -= 100
        rightMotorSpeed -= 100
    if 'd' in pressedKeys and 'a' not in pressedKeys:
        if 'w' in pressedKeys and \
            's' not in pressedKeys:
            rightMotorSpeed -= 50
        elif 's' in pressedKeys and \
            'w' not in pressedKeys:
            rightMotorSpeed += 50
        else:
            rightMotorSpeed -= 100
            leftMotorSpeed += 100
    if 'a' in pressedKeys and 'd' not in pressedKeys:
        if 'w' in pressedKeys and \
            's' not in pressedKeys:
            leftMotorSpeed -= 50
        elif 's' in pressedKeys and \
            'w' not in pressedKeys:
            leftMotorSpeed += 50
        else:
            leftMotorSpeed -= 100
            rightMotorSpeed += 100
    if 'h' in pressedKeys:
        handMotorSpeed += 100

    sock.sendto(bytes("%d, %d, %d" % \
        (leftMotorSpeed, rightMotorSpeed, handMotorSpeed), \
        "UTF-8"), address)
    print("pressed:", pressedKeys)
    
keyboard.hook(keyEvent)

i=0
while True:
    i += 1
