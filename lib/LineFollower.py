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
        self._tspd = -240
        self._gyroTreshold = 20
        self._repositionTime = 0.75
        self._lineFollowTime = 1.5
        self._operation = RobotInterface.DriveForward(robot=self._robot, distance=0.05)

    def Update(self):
        if self._operation is RobotInterface.GyroPivot and self._operation.update():
            self.operation = RobotInterface.DriveForward(robot=self._robot, speed=-200, distance=0.10)
        if self._colorSensor.value() < self._bright:
            self.operation = (
                RobotInterface.GyroPivot(robot=self._robot, angle_diff=-5),
                RobotInterface.GyroPivot(robot=self._robot, angle_diff=5)
            )
        else:
            self.operation = RobotInterface.DriveForward(robot=self._robot, distance=0.05)

        return self.Id

    def Enter(self):
        super().Enter()
        self._colorSensor.mode = 'COL-REFLECT'
        self._gyro.mode = 'GYRO-ANG'


    def Exit(self):
        super().Exit()
        self._robot.stop()
