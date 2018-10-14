from lib import obj_pipe
from lib import vec2

dir = vec2.Vec2(1.0, 0.0)
client = obj_pipe.send(("localhost", 8001))

while True:
    dir = dir.rotate(0.01)
    client(dir)
