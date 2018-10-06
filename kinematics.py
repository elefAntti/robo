from collections import namedtuple
from math import sin, cos
from vec2 import Vec2, Transform


class Command(namedtuple("command", ["velocity", "angularVelocity"])):
    __slots__ = ()
    #Limit for when the movement is considered straight
    max_straight_curvature = 0.001
    #Limit for when the movement is considered stopped
    max_stopped_velocity = 0.0001

    @staticmethod
    def arc(velocity, curvature):
        return Command(
            velocity = velocity,
            angularVelocity = velocity * curvature)

    @property
    def straight(self):
        return not self.pivot and \
            abs(self.curvature) < Command.max_straight_curvature

    @property
    def pivot(self):
        return abs(self.velocity) < Command.max_stopped_velocity

    @property
    def radius(self):
        return self.velocity / self.angularVelocity

    @property
    def curvature(self):
        return self.angularVelocity / self.velocity

WheelCommand = namedtuple("WheelCommand", ["left_angular_vel", "right_angular_vel"])

class KinematicModel:
    slots = ("axel_width", "left_wheel_r", "right_wheel_r")
    def __init__(self, axel_width, left_wheel_r, right_wheel_r):
        self.axel_width = axel_width
        self.left_wheel_r = left_wheel_r
        self.right_wheel_r = right_wheel_r

    def computeWheelCommand(self, command):
        r = self.axel_width / 2 
        right_vel = command.velocity + r * command.angularVelocity
        left_vel = command.velocity - r * command.angularVelocity

        return WheelCommand(
            left_angular_vel = left_vel / self.left_wheel_r,
            right_angular_vel = right_vel / self.right_wheel_r)

    def computeCommand(self, wheel_command):
        left_vel = wheel_command.left_angular_vel * self.left_wheel_r
        right_vel = wheel_command.right_angular_vel * self.right_wheel_r

        angularVelocity = (right_vel - left_vel) / self.axel_width
        velocity = (right_vel + left_vel) / 2.0

        return Command(velocity, angularVelocity)

def predictPose(pose, command, time):
    if command.pivot:
        return Transform(
            heading = pose.heading + command.angularVelocity * time,
            offset = pose.offset)
    elif command.straight:
        distance = command.velocity * time
        return Transform(
            heading = pose.heading, 
            offset = pose.offset + Vec2.fromPolar(pose.heading, distance))
    else:
        new_heading = pose.heading + command.angularVelocity * time
        displacement = Vec2(
            x = (sin(new_heading) - sin(pose.heading)),
            y = (-cos(new_heading) + cos(pose.heading))
        ) * command.radius
        return Transform(
            heading=new_heading,
            offset=pose.offset + displacement)
