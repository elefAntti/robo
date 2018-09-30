from copy import copy
from math import sin, cos


class Command:
    def __init__(self, velocity, curvature):
        self.velocity = velocity
        self.curvature = curvature

    def __copy__(self):
        return type(self)(self.velocity, self.curvature)

    def __repr__(self):
        return "Command({}, {})".format(self.velocity, self.curvature)

    @property
    def straight(self):
        return abs(self.curvature) < 0.001

    @property
    def radius(self):
        return 1/self.curvature

    @property
    def angularVelocity(self):
        return self.velocity * self.curvature

    @property
    def pivot(self):
        return False


class PivotCommand:
    def __init__(self, angular_vel):
        self.angularVelocity = angular_vel

    def __copy__(self):
        return type(self)(self.angularVelocity)

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


class Pose:
    def __init__(self, x, y, heading):
        self.x = x
        self.y = y
        self.heading = heading

    def __copy__(self):
        return type(self)(self.x, self.y, self.heading)

    def __repr__(self):
        return "Pose({}, {}, {})".format(self.x, self.y, self.heading)


class WheelCommand:
    def __init__(self, left_angular_vel, right_angular_vel):
        self.left_angular_vel = left_angular_vel
        self.right_angular_vel = right_angular_vel


class KinematicModel:
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
            left_vel = left_radius * commmand.angularVelocity
            right_vel = right_radius * command.angularVelocity
        left_angular_vel = left_vel / self.left_wheel_r
        right_angular_vel = right_vel / self.right_wheel_r
        return WheelCommand(left_angular_vel, right_angular_vel)

    def computeCommand(self, wheel_command):
        left_vel = wheel_command.left_angular_vel * self.left_wheel_r
        right_vel = wheel_command.right_angular_vel * self.right_wheel_r
        if abs(left_vel + right_vel) < 0.0001:
            return PivotCommand(right_vel / (self.axel_width / 2))

        curvature = (left_vel - right_vel) / (left_vel + right_vel) \
            / (self.axel_width / 2)
        command = Command(1.0, curvature)
        if command.straight:
            command.velocity = left_vel
        else:
            angular_vel = left_vel / self.left_wheel_r
            command.velocity = angular_vel / curvature
        return command


def predictPose(pose, command, time):
    new_pose = copy(pose)
    if command.pivot:
        new_pose.heading += command.angularVelocity * time
    elif command.straight:
        distance = command.velocity * time
        new_pose.x += cos(pose.heading) * distance
        new_pose.y += sin(pose.heading) * distance
    else:
        new_pose.heading += command.angularVelocity * time
        new_pose.x += (sin(new_pose.heading) - sin(pose.heading)) \
            * command.radius
        new_pose.y += (-cos(new_pose.heading) + cos(pose.heading)) \
            * command.radius
    return new_pose
