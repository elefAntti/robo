from ev3dev import ev3
from .vec2 import Vec2, Transform
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
        print("GyroPivot! %f"% robot.gyro.value())
        print("target %f"% self.target_angle)
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

class GyroOdometry:
    wheel_radius = 38 / 2
    def __init__(self, robo):
        self.reset(robo)
    def reset(self, robo):
        self.left_position = robo.left_motor.position
        self.right_position = robo.right_motor.position
        self.gyro_angle = robo.gyro.angle
        self.position = Vec2.zero()
    def update(self, robo):
        new_left = robo.left_motor.position 
        new_right = robo.right_motor.position
        new_angle = robo.gyro.angle
        d_left = (new_left - self.left_position) / 180.0 * math.pi
        d_right = (new_right - self.right_position) / 180.0 * math.pi
        forward = (d_left + d_right) * self.wheel_radius
        mid_angle = (new_angle + self.gyro_angle) / 2.0
        delta = Vec2.fromPolar(mid_angle, forward)
        self.position = self.position + delta
        self.gyro_angle = new_angle
    def get_transform(self):
        return Transform(heading = self.gyro_angle, offset = self.position)

class RobotInterface:
    def __init__(self, left_port, right_port, max_speed = 700, flip_dir=False):
        self.left_motor = ev3.LargeMotor(left_port)
        self.right_motor = ev3.LargeMotor(right_port)
        self.sound = ev3.Sound()

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
            self.colorSensor = ev3.ColorSensor('in3')
            self.colorSensor.mode = 'COL-REFLECT'
        except:
            self.colorSensor = None
            print("Color sensor not found")

        try:
            self.frontColorSensor = ev3.ColorSensor('in1')
            self.frontColorSensor.mode = 'COL-COLOR'
        except:
            self.frontColorSensor = None
            print("Front color sensor not found")

        try:
            self.ultrasonicSensor = ev3.UltrasonicSensor()
            self.ultrasonicSensor.mode = 'US-DIST-CM'
        except:
            self.ultrasonicSensor = None
            print("Ultrasonic sensor not found")

        self.max_speed = max_speed
        self.flip_dir = flip_dir
        self.log = open("sensor.log", "w+")

    def logStuff(self):
        log.write("%f, %f, %f"% \
            (self.gyro.angle, self.left_motor.position, self.right_motor.position))

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
