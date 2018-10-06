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

    @staticmethod
    def arc_to(from_pose, to_vec, speed):
        vec_in_local = from_pose.inverse().applyTo(to_vec)
        behind = vec_in_local.x < 0
        return Command.arc( velocity = speed if not behind else -speed,
            curvature = 2.0 * vec_in_local.y / vec_in_local.lengthSq)

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

    def integrate(self, time):
        if self.straight:
            distance = self.velocity * time
            return Transform.translation(Vec2(distance, 0))
        else:
            heading_change = self.angularVelocity * time
            displacement = Vec2.zero() if self.pivot else \
                self.radius * Vec2(
                    x = sin(heading_change),
                    y = (-cos(heading_change) + 1))
            return Transform(
                heading=heading_change,
                offset=displacement)

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
    return pose.after(command.integrate(time))