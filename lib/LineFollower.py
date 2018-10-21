from lib.state import State, States
from lib.enums import Colors
from lib import RobotInterface
import time

class LineFollower(State):

    def __init__(self, id, environment):
        super().__init__(id, environment)
        self._colorSensor = self._robot.colorSensor
        self._gyro = self._robot.gyro
        self._turn = -200
        self._bright = 15
        self._tspd = -480
        self._gyroTreshold = 15
        self._turnRight = True
        self._lastGyro = 0
        self._turnMode = False
        self._repositionTime = 0.35
        self._lineFollowTime = 1.5
        self._operation = None
        self._operName = 'none'
        self._lineFollowTimer = 0
        self._sequence = [-90, -90, 90, 90, 45, 45, 180, -90, -90, 90, 90, -90]
        self._sequenceIdx = 0

    def Update(self):
        if self._operName == 'forward':
            if self._operation.update():
                self._operation = RobotInterface.GyroPivot(self._robot, 90 if self._turnRight else -90)
                self._operName = 'pivot'
        elif self._operName == 'pivot':
            if self._operation.update():
                self._operation = None
                self._operName = 'none'
                self._lineFollowTimer = time.time()
                self._lastGyro = self._gyro.value()
        else:
            #print(self._colorSensor.value())        
            rspd = 0
            if self._colorSensor.mode == 'COL-REFLECT':
                sensorValue = self._colorSensor.value()
            else:
                sensorValue = self._colorSensor.value(0) / 3.0
            if sensorValue > self._bright:
                rspd = -self._turn if self._sequenceIdx <= 6 else self._turn
                if not self._turnRight:
                    self._turnRight = True
                    self._lastGyro = self._gyro.value()
            else:
                rspd = self._turn if self._sequenceIdx <= 6 else -self._turn
                if self._turnRight:
                    self._turnRight = False
                    self._lastGyro = self._gyro.value()

            #print((time.time() - self._lineFollowTimer), (abs(self._lastGyro - self._gyro.value())))
            if self._sequenceIdx != 6 and abs(self._lastGyro - self._gyro.value()) > self._gyroTreshold and time.time() - self._lineFollowTimer > self._lineFollowTime:
                #self._robot.driveForTime(500, 500, self._repositionTime)
                self._operation = RobotInterface.GyroPivot(self._robot, 100 if self._turnRight else -100)
                self._operation.target_angle = (self._lastGyro * -1) - self._sequence[self._sequenceIdx]
                self._sequenceIdx += 1
                self._colorSensor.mode = 'RGB-RAW' if self._sequenceIdx == 6 else 'COL-REFLECT'
                self._operName = 'pivot'
            if self._sequenceIdx == 6 and self._colorSensor.mode == 'RGB-RAW' and self._colorSensor.value(0) > 100 and self._colorSensor.value(2) < 100:
                self._robot.driveForTime(500, 500, 1)
                time.sleep(2)
                self._robot.driveForTime(-500, -500, 2.5)
                self._sequenceIdx += 1
                self._colorSensor.mode = 'COL-REFLECT'
                self._operation = None
                self._operName = 'none'
                self._lineFollowTimer = time.time()
                self._lastGyro = self._gyro.value()
            right = (self._tspd + rspd)/2.0
            left = self._tspd - right
            self._robot.simpleDrive(-left, -right)

        return self.Id

    def Enter(self):
        super().Enter()
        self._colorSensor.mode = 'COL-REFLECT'
        self._gyro.mode = 'GYRO-ANG'
        self._turnRight = True
        self._lastGyro = self._gyro.value()
        self._turnMode = False
        self._lineFollowTimer = time.time()
        self._operName = 'none'
        self._sequenceIdx = 0

    def Exit(self):
        super().Exit()
        self._robot.stop()
