from ev3dev import ev3
import time

class RobotInterface:
    
    def __init__(self, left_port, right_port, max_speed = 700, flip_dir=False):
        self.left_motor = ev3.LargeMotor(left_port)
        self.right_motor = ev3.LargeMotor(right_port)
        self.sound = ev3.Sound()
        try:
            self.sound.beep()
            time.sleep(2)
            self.gyro = ev3.GyroSensor()
            self.gyro.mode='GYRO-ANG'
            time.sleep(2)
            self.sound.beep()
        except:
            self.gyro = None
            print("Gyro not found")
        self.max_speed = max_speed
        self.flip_dir = flip_dir
        self.log = open("sensor.log", "w+")

    def logStuff(self):
        self.log.write("%f, %f, %f"% \
            (self.gyro.value(), self.left_motor.position, self.right_motor.position))

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
    
    def stop(self):
        left_motor.stop()
        right_motor.stop()