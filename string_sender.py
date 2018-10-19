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

while True:
    data = input('Send message of type "(1) (2)", (1) is cmd (2) is timeout: ')
    #print(data.split())
    sock.sendto(bytes(data, "UTF-8"), address)