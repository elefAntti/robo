from collections import namedtuple
from math import sin, cos
from vec2 import Vec2, Transform

#Limit for when the movement is considered straight
max_straight_curvature = 0.001

class Command(namedtuple("command", ["velocity", "curvature"])):
    __slots__ = ()

    @property
    def straight(self):
        return abs(self.curvature) < max_straight_curvature

    @property
    def radius(self):
        return 1/self.curvature

    @property
    def angularVelocity(self):
        return self.velocity * self.curvature

    @property
    def pivot(self):
        return False


class PivotCommand(namedtuple("PivotCommand", ["angularVelocity"])):
    __slots__ = ()

    @property
    def straight(self):
        return False

    @property
    def radius(self):
        return 0.0

    @property
    def velocity(self):
        return 0.0

    @property
    def pivot(self):
        return True

WheelCommand = namedtuple("WheelCommand", ["left_angular_vel", "right_angular_vel"])

class KinematicModel:
    slots = ("axel_width", "left_wheel_r", "right_wheel_r")
    def __init__(self, axel_width, left_wheel_r, right_wheel_r):
        self.axel_width = axel_width
        self.left_wheel_r = left_wheel_r
        self.right_wheel_r = right_wheel_r

    def computeWheelCommand(self, command):
        if command.pivot:
            right_vel = self.axel_width / 2 * command.angularVelocity
            left_vel = -self.axel_width / 2 * command.angularVelocity
        elif command.straight:
            left_vel = command.velocity
            right_vel = command.velocity
        else:
            left_radius = command.radius - self.axel_width / 2
            right_radius = command.radius + self.axel_width / 2
            left_vel = left_radius * command.angularVelocity
            right_vel = right_radius * command.angularVelocity

        return WheelCommand(
            left_angular_vel = left_vel / self.left_wheel_r,
            right_angular_vel = right_vel / self.right_wheel_r)

    def computeCommand(self, wheel_command):
        left_vel = wheel_command.left_angular_vel * self.left_wheel_r
        right_vel = wheel_command.right_angular_vel * self.right_wheel_r
        if abs(left_vel + right_vel) < 0.0001:
            return PivotCommand(right_vel / (self.axel_width / 2))

        curvature = (left_vel - right_vel) / (left_vel + right_vel) \
            / (self.axel_width / 2)

        if abs(curvature) < max_straight_curvature:
            return Command(
                velocity = left_vel,
                curvature = 0.0)
        else:
            angular_vel = left_vel / self.left_wheel_r
            return Command(
                velocity=angular_vel / curvature,
                curvature=curvature)


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
        offset=pose.offset + displacement
    )
