import rx
import socket
import pickle

def listen(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(address)
    def server(observer):
        while True:
            data, addr = sock.recvfrom(4096)
            observer.on_next(pickle.loads(data))
    return rx.Observable.create(server)

def send(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    def client(data):
        sock.sendto(pickle.dumps(data), address)
    return client