import socket
import time

class RemoteControlSocket:
    safety_time = 3.0
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ("", 8000)
        self.sock.bind(server_address)
        self.sock.setblocking(0)
        self.message = [-1,0,0,0]
        self.last_received = time.time()
    def receive(self):
        try:
            data, client = self.sock.recvfrom(128)
            data = data.decode("utf-8")
            #print("Received remote: %s"%str(data))
            new_message = [float(x) for x in data.split(",")]
            #The index 0 is the sequence number
            if new_message[0] < 10 or new_message[0] > self.message[0]:
                self.message = new_message
                self.last_received = time.time()
        except:
            pass
        return self.message[1:]
    def is_timeout(self):
        return time.time() - self.last_received > safety_time