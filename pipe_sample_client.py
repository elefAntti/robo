import rx
from time import sleep
from lib import obj_pipe
from lib import vec2

dir = vec2.Vec2(1.0, 0.0)

client = obj_pipe.send(("localhost", 8001))

rx.Observable.interval(20) \
    .scan(lambda dir, _:dir.rotate(0.01),
    vec2.Vec2(1.0, 0.0)) \
    .subscribe(client)

while True:
    sleep(0.01)

