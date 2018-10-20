from lib.state import State, States
from lib.enums import Colors
from lib import RobotInterface
import time

class LineFollower(State):

    def __init__(self, id, environment):
        super().__init__(id, environment)
        self._colorSensor = self._robot.colorSensor
        self._gyro = self._robot.gyro
        self._turn = 200
        self._bright = 15
        self._tspd = -120
        self._gyroTreshold = 20
        self._turnRight = True
        self._lastGyro = 0
        self._turnMode = False
        self._repositionTime = 0.75
        self._lineFollowTime = 1.5
        self._operation = None
        self._lineFollowTimer = 0

    def Update(self):
        if self._operation is RobotInterface.DriveForward:
            if self._operation.update():
                self._operation = self._operation = RobotInterface.GyroPivot(self._robot, 80 if self._turnRight else -80)
        elif self._operation is RobotInterface.GyroPivot:
            if self._operation.update():
                self._operation = None
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

            if abs(self._lastGyro - self._gyro.value()) > self._gyroTreshold and time.time() - self._lineFollowTimer > self._lineFollowTime:
                #self._robot.driveForTime(500, 500, self._repositionTime)
                self._operation = RobotInterface.DriveForward(self._robot, 0.13)
            right = (self._tspd + rspd)/2.0
            left = self._tspd - right
            self._robot.simpleDrive(-left, -right)

        return self.Id

    def Enter(self):
        self._sound.speak("Entering " + self.Id.name)
        self._colorSensor.mode = 'COL-REFLECT'
        self._gyro.mode = 'GYRO-ANG'
        self._turnRight = True
        self._lastGyro = self._gyro.value()
        self._turnMode = False
        self._lineFollowTimer = time.time()

    def Exit(self):
        self._sound.speak("Exiting " + self.Id.name)
        self._robot.stop()
