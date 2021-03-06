from ev3dev import ev3
from .vec2 import Vec2, Transform
from .kinematics import Command
import time
import math

#def getDifference(b1, b2):
#	r = (b2 - b1) % 360.0
#	# Python modulus has same sign as divisor, which is positive here,
#	# so no need to consider negative case
#	if r >= 180.0:
#		r -= 360.0
#	return r

class GyroPivot:
    def __init__(self, robot, angle_diff, speed = 150, accuracy = 1):
        self.start_angle = robot.gyro.value() * -1
        self.target_angle = self.start_angle + angle_diff
        self.robot = robot
        self.speed = speed
        self.accuracy = accuracy
        self.angle_diff = angle_diff
        self.start()
    def start(self):
        self.start_angle = self.robot.gyro.value() * -1
        self.target_angle = self.start_angle + self.angle_diff
    def update(self):
        dAngle = self.target_angle - self.robot.gyro.value() * -1
        k = max(abs(dAngle / 10), 1)
        speed = self.speed * k
        if abs(dAngle) < self.accuracy:
            self.robot.stop()
            return True
        if dAngle < 0:
            self.robot.simpleDrive(speed, -speed)
        else:
            self.robot.simpleDrive(-speed, speed)
        return False
      
class GyroWaitForRotation:
    def __init__(self, robot, angle_diff):
        self.target_angle = self.start_angle + angle_diff
        self.robot = robot
        self.angle_diff = angle_diff
        self.start()
    def start(self):
        self.target_angle = self.robot.gyro_angle_deg + self.angle_diff
    def update(self):
        if self.angle_diff == 0:
            return True 
        if self.angle_diff > 0 and self.robot.gyro_angle_deg > self.target_angle:
            return True
        if self.angle_diff < 0 and self.robot.gyro_angle_deg < self.target_angle:
            return True
        return False

# need to move backwards? distance and speed should be BOTH negative
class DriveForward:
    def __init__(self, robot, distance, speed = 200, accuracy = 0.01):
        self.robot = robot
        self.speed = speed
        self.accuracy = accuracy
        self.distance = distance
        self.start()
    def start(self):
        self.left_position = self.robot.left_motor_pos
        self.right_position = self.robot.right_motor_pos
    def update(self):
        new_left = self.robot.left_motor_pos
        new_right = self.robot.right_motor_pos
        d_left = (new_left - self.left_position) / 180.0 * math.pi
        d_right = (new_right - self.right_position) / 180.0 * math.pi
        forward = (d_left * self.robot.kinematics.left_wheel_r\
         + d_right * self.robot.kinematics.right_wheel_r) / 2.0

        diff = self.distance - forward
        if abs(diff) < self.accuracy:
            self.robot.stop()
            return True
        k = max(abs(diff / 0.10), 1)
        speed = self.speed * k 
        self.robot.simpleDrive(speed, speed)
        return False

class DriveToAWall:
    def __init__(self, robot, speed = 200, both_sensors = False):
        self.robot = robot
        self.speed = speed
        self.both_sensors = both_sensors
        self.start()
    def start(self):
        pass
    def update(self):
        self.robot.simpleDrive(self.speed, self.speed)
        if self.robot.left_push_sensor.value() or self.robot.right_push_sensor.value():
            return not self.both_sensors
        if self.robot.left_push_sensor.value() and self.robot.right_push_sensor.value():
            return True        
        return False

#Waits for the robot to move a given distance, kind of useless by it self but used in other tasks
class WaitForDistance:
    def __init__(self, robot, distance, accuracy = 0.01):
        self.robot = robot
        self.accuracy = accuracy
        self.distance = distance
        self.start()
    def start(self):
        self.left_position = self.robot.left_motor_pos
        self.right_position = self.robot.right_motor_pos
    def update(self):
        new_left = self.robot.left_motor_pos
        new_right = self.robot.right_motor_pos
        d_left = (new_left - self.left_position) / 180.0 * math.pi
        d_right = (new_right - self.right_position) / 180.0 * math.pi
        forward = (d_left * self.robot.kinematics.left_wheel_r\
         + d_right * self.robot.kinematics.right_wheel_r) / 2.0

        diff = self.distance - forward
        if abs(diff) < self.accuracy:
            self.robot.stop()
            return True
        return False

class LineFollowCommand:
    def __init__(self, robot, distance, accuracy = 0.01):
        self.robot = robot
        self._tspd = -240
        self._bright = 150
        self._turn = 50
        self.wait = WaitForDistance(robot, distance, accuracy)
    def start(self):
        self.wait.start()
    def update(self):
        if self.wait.update():
            return True
        if self.robot.colorSensor.value() > self._bright:
            rspd = -self._turn
        else:
            rspd = self._turn
        right = (self._tspd + rspd)/2.0
        left = self._tspd - right
        self.robot.simpleDrive(-left, -right)
        return False

class GyroOdometry:
    wheel_radius = 38 / 2
    def __init__(self, robo):
        self.reset(robo)
    def reset(self, robo):
        self.left_position = robo.left_motor_pos
        self.right_position = robo.right_motor_pos
        self.gyro_angle = robo.gyro_angle_rad
        self.position = Vec2.zero()
    def update(self, robo):
        new_left = robo.left_motor_pos
        new_right = robo.right_motor_pos
        new_angle = robo.gyro_angle_rad
        d_left = (new_left - self.left_position) / 180.0 * math.pi
        d_right = (new_right - self.right_position) / 180.0 * math.pi
        forward = (d_left + d_right) * self.wheel_radius
        mid_angle = (new_angle + self.gyro_angle) / 2.0
        delta = Vec2.fromPolar(mid_angle, forward)
        self.position = self.position + delta
        self.gyro_angle = new_angle
    def get_transform(self):
        return Transform(heading = self.gyro_angle, offset = self.position)


class ArcWithGyro:
    def __init__(self, robot, target, speed = 200, accuracy = 0.1):
        self.robot = robot
        self.speed = speed
        self.accuracy = accuracy
        self.target = target
        self.gyro_odo = GyroOdometry(robot)
        self.start()
    def start(self):
        self.gyro_odo.reset(self.robot)

    def update(self):
        self.gyro_odo.update(self.robot)
        dist = self.target.distance(self.gyro_odo.get_transform().offset)
        if dist < self.accuracy:
            self.robot.stop()
            return True

        k = max(abs(dist / 0.10), 1)
        speed = self.speed * k 
        command = Command.arc_to(self.gyro_odo.get_transform(), self.target, speed)
        wheel_command = self.robot.kinematics.computeWheelCommand(command)
        self.robot.executeWheelCommand(wheel_command)
        return False

class RobotInterface:
    def __init__(self, left_port, right_port, kinematics, max_speed = 700, flip_dir=False):
        self.left_motor = ev3.LargeMotor(left_port)
        self.right_motor = ev3.LargeMotor(right_port)
        self.sound = ev3.Sound()
        self.kinematics = kinematics

        try:
            self.sound.beep()
            self.gyro = ev3.GyroSensor()
            self.gyro.mode='GYRO-CAL'
            time.sleep(2)

            self.gyro.mode='GYRO-ANG'

            time.sleep(2)
            self.sound.beep()
        except:
            self.gyro = None
            print("Gyro not found")

        try:
            self.colorSensor = ev3.ColorSensor('in2')
            self.colorSensor.mode = 'COL-REFLECT'
        except:
            self.colorSensor = None
            print("Color sensor not found")

        try:
            self.left_push_sensor = ev3.TouchSensor('in3')
        except:
            self.left_push_sensor = None
            print("Left push sensor not found.")

        self.frontColorSensor = None

        try:
            self.right_push_sensor = ev3.TouchSensor('in1')
        except:
            self.right_push_sensor = None
            print("Right push sensor not found.")

        try:
            self.ultrasonicSensor = ev3.UltrasonicSensor()
            self.ultrasonicSensor.mode = 'US-DIST-CM'
        except:
            self.ultrasonicSensor = None
            print("Ultrasonic sensor not found")

        self.max_speed = max_speed
        self.flip_dir = flip_dir
        self.log = open("sensor.log", "w+")

    @property
    def left_motor_pos(self):
        direction = -1 if self.flip_dir else 1
        return self.left_motor.position * direction

    @property
    def right_motor_pos(self):
        direction = -1 if self.flip_dir else 1
        return self.right_motor.position * direction

    @property
    def gyro_angle_deg(self):
        if self.gyro:
            return self.gyro.value() * -1
        else:
            return 0

    @property
    def gyro_angle_rad(self):
        return self.gyro_angle_deg * math.pi / 180.0

    def simpleDrive(self, left_speed, right_speed):
        limiting_speed = max(abs(left_speed), abs(right_speed))
        scale = self.max_speed/limiting_speed if limiting_speed > self.max_speed else 1
        left_speed *= scale
        right_speed *= scale
        if self.flip_dir:
            left_speed *= -1
            right_speed *= -1     
        if abs(left_speed) == 0:
            self.left_motor.stop()
        else:
            self.left_motor.run_forever(speed_sp = left_speed)
        if abs(right_speed) == 0:
            self.right_motor.stop()
        else:
            self.right_motor.run_forever(speed_sp = right_speed)
        #print( "L=%f, R=%f" % (left_speed, right_speed) )

    def executeWheelCommand(self, command):
        self.simpleDrive(command.left_angular_vel * 180.0 / math.pi,
            command.right_angular_vel * 180.0 / math.pi)

    def driveForwards(self, speed):
        self.simpleDrive(abs(speed), abs(speed))

    def driveBackwards(self, speed):
        self.simpleDrive(-abs(speed), -abs(speed))

    def driveForTime(self, left_speed, right_speed, driveTime):
        self.simpleDrive(left_speed, right_speed)
        time.sleep(driveTime)
        self.stop()

    def driveForwardsForDistance(self, speed, distance):
        driveTime = distance / speed
        self.driveForTime(abs(speed), abs(speed), driveTime)

    def driveBackwardsForDistance(self, speed, distance):
        driveTime = distance / speed
        self.driveForTime(-abs(speed), -abs(speed), driveTime)
    
    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()
    
    def resetOdometry(self):
        self.left_motor.position = 0
        self.right_motor.position = 0


class CommandSequence:
    def __init__(self, *children):
        self.children = children
        self.start()
    def start(self):
        self.currentChild = 0
        self.children[self.currentChild].start()
    def update(self):
        if self.currentChild >= len(self.children):
            return True
        done = self.children[self.currentChild].update()
        if done:
            self.currentChild += 1
            if self.currentChild >= len(self.children):
                return True
            self.children[self.currentChild].start()
        return False

class WaitCommand:
    def __init__(self, robot, duration):
        self.robot = robot
        self.duration = duration
        self.start()
    def start(self):
        self.start_time = time.time()
        self.robot.stop()
    def update(self):
        return (time.time() - self.start_time) >= self.duration

class GyroInitCommand:
    def __init__(self, robot):
        self.robot = robot
        #self.start()
    def start(self):
        self.start_time = time.time()
        self.robot.sound.beep()
        self.robot.gyro.mode='GYRO-CAL'
    def update(self):
        if (time.time() - self.start_time) >= 2:
            self.robot.gyro.mode='GYRO-ANG'
            self.robot.sound.beep()
            return True
        return False


