from lib import vec2
from lib import obj_pipe
from time import sleep

server = obj_pipe.listen(("localhost", 8001)) 

@obj_pipe.decoder(vec2.Vec2)
def decodeVec2(msg):
    return vec2.Vec2(*msg)

server.subscribe(print)

while True:
    sleep(0.01)