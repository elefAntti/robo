import socket

class RemoteControlSocket:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ("", 8000)
        self.sock.bind(server_address)
    def receive(self):
        data, client = self.sock.recvfrom(64)
        data = data.decode("utf-8")
        print("Received remote: %s"%str(data))
        return [float(x) for x in data.split(",")]