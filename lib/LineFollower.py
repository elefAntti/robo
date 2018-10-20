from lib.state import State, States
from lib.enums import Colors
from lib import RobotInterface
import time

class LineFollower(State):

    def __init__(self, id, environment):
        super().__init__(id, environment)
        self._robot = environment["robot"]
        self._colorSensor = self._robot.colorSensor
        self._gyro = self._robot.gyro
        self._turn = 200
        self._bright = 15
        self._tspd = -120
        self._gyroTreshold = 20
        self._turnRight = True
        self._lastGyro = 0
        self._turnMode = False

    def Update(self):
        if self._turnMode:
            operation = RobotInterface.GyroPivot(self._robot, 90 if self._turnRight else -90)
            if operation.update():
                self._turnMode = False
        else:
            print(self._colorSensor.value())        
            rspd = 0
            if self._colorSensor.value() > self._bright:
                rspd = -self._turn
                if not self._turnRight:
                    self._turnRight = True
                    self._lastGyro = self._gyro.value()
            else:
                rspd = self._turn
                if self._turnRight:
                    self._turnRight = False
                    self._lastGyro = self._gyro.value()

            if abs(self._lastGyro - self._gyro.value()) > self._gyroTreshold:
                self._robot.driveForTime(500, 500, 0.25)
                self._turnMode = True
            right = (self._tspd + rspd)/2.0
            left = self._tspd - right
            self._robot.SimpleDrive(left, right)

        return self.Id

    def Enter(self):
        self._colorSensor.mode = 'COL-REFLECT'
        self._gyro.mode = 'GYRO-ANG'
        self._turnRight = True
        self._lastGyro = self._gyro.value()
        self._turnMode = False

    def Exit(self):
        self._robot.stop()
