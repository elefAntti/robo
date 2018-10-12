import vec2
import obj_pipe
from time import sleep

server = obj_pipe.listen(("localhost", 8001)) 

server.subscribe(print)

while True:
    sleep(0.01)