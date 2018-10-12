
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

address =('169.254.45.0', 8000)
print("Sending")
#sock.bind(server_address)

sent = sock.sendto(bytes("Foobar", "UTF-8"), address)

while True:
    sent = sock.sendto(bytes("Foobar", "UTF-8"), address)
    print("sent " + str(sent))