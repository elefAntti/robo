import socket
import sys
import keyboard
pressedKeys = []
ip = '192.168.2.3'

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = (ip, 8000)

def keyEvent(ke):
    key = ke.name
    typ = ke.event_type
    if typ == 'down':
        if key == 'w' and 'w' not in pressedKeys:
            sent = sock.sendto(bytes("forw", "UTF-8"), address)
            pressedKeys.append('w')
        if key == 's' and 's' not in pressedKeys:
            sent = sock.sendto(bytes("back", "UTF-8"), address)
            pressedKeys.append('s')
        if key == 'a' and 'a' not in pressedKeys:
            sent = sock.sendto(bytes("left", "UTF-8"), address)
            pressedKeys.append('a')
        if key == 'd' and 'd' not in pressedKeys:
            sent = sock.sendto(bytes("right", "UTF-8"), address)
            pressedKeys.append('d')
    if typ == 'up' and key in pressedKeys:
        pressedKeys.remove(key)
    if typ == 'up' and key in ['w','a','s','d'] and 'w' not in pressedKeys and 's' not in pressedKeys and 'a' not in pressedKeys and 'd' not in pressedKeys:
        sent = sock.sendto(bytes("halt", "UTF-8"), address)
    #print(sent)
keyboard.hook(keyEvent)

i=0
while True:
    i += 1
