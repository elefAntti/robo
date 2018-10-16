import rx
from rx.concurrency import ThreadPoolScheduler
import socket
import msgpack

scheduler = ThreadPoolScheduler()
handshake_len = 10

_decoders = {}

#Decorator
def decoder(Class):
    def register(fun):
        _decoders[Class.__name__] = fun
        return fun 
    return register

def decode(msg):
    class_name = str(msg[1])
    if class_name in _decoders:
        return _decoders[class_name](msg[2])
    else:
        return msg[2]

def listen(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(address)
    def server(observer):
        msg_counter = 0
        while True:
            data, addr = sock.recvfrom(4096)
            msg = msgpack.loads(data, encoding = "utf-8")
            if msg_counter < msg[0] or msg[0] < handshake_len:
                msg_counter = msg[0]
                observer.on_next(decode(msg))
    return rx.Observable.create(server).subscribe_on(scheduler) 

def send_raw(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(0)
    def client(data):
        sock.sendto(msgpack.dumps(data, encoding = "utf-8"), address)
    return client

def send(address):
    observable = rx.subjects.Subject()
    raw_client = send_raw(address)
    encode = lambda obj, counter: (counter, obj.__class__.__name__, obj)
    observable.map(encode).subscribe(raw_client)
    return observable
        