import socket
import sys
import keyboard
pressedKeys = []

ip = '192.168.2.3'

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = (ip, 8000)

def keyEvent(ke):
    leftMotorSpeed = 0
    rightMotorSpeed = 0
    handMotorSpeed = 0
    key = ke.name
    typ = ke.event_type
    if typ == 'down':
        if key not in pressedKeys:
            pressedKeys.append('w')
    if typ == 'up' and key in pressedKeys:
        pressedKeys.remove(key)

    
    if 'w' in pressedKeys and 's' not in pressedKeys:
        leftMotorSpeed += 100
        rightMotorSpeed += 100
    if 's' in pressedKeys and 'w' not in pressedKeys:
        leftMotorSpeed -= 100
        rightMotorSpeed -= 100
    if 'd' in pressedKeys:
        if 's' not in pressedKeys:
            rightMotorSpeed -= 50
        elif 'w' in pressedKeys:
            rightMotorSpeed += 50
        else:
    if 'a' in pressedKeys:
        if 's' not in pressedKeys:
            leftMotorSpeed -= 50
        if 'w' not in pressedKeys:
            leftMotorSpeed += 50
    if 'h' in pressedKeys:
        handMotorSpeed += 100

    sent = sock.sendto(bytes("%d, %d, %d" % (leftMotorSpeed, rightMotorSpeed, handMotorSpeed),
        "UTF-8"), address)
    print("pressed:", pressedKeys)
    
keyboard.hook(keyEvent)

i=0
while True:
    i += 1
