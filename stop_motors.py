#!/usr/bin/env python3

from ev3dev import ev3

print("Stopping motors")
lmotor = ev3.LargeMotor('outB')
rmotor = ev3.LargeMotor('outA')
lmotor.stop()
rmotor.stop()
print("Motors stopped")