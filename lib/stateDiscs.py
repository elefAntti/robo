from lib.state import State, States
from lib.enums import Colors
from lib.RobotInterface import *


## 0.7, -0.7
## 1.4, 0.0

class StateDiscs(State):
    def __init__(self, id, environment):
        super().__init__(id, environment)
        robot_len = 0.17
        self.command_sequence = CommandSequence(
            WaitCommand(self._robot, 0.5),
            GyroInitCommand(self._robot),
            DriveForward(self._robot, 0.422 + robot_len),
            GyroWaitForRotation(self._robot, -80 ),
            DriveForward(self._robot, (0.03 + 2* robot_len)*-1, speed=-200),
            GyroWaitForRotation(self._robot, -200 ),
            DriveForward(self._robot, 0.03 + 2*robot_len),
            GyroWaitForRotation(self._robot, -100 ),
            DriveForward(self._robot, (0.13 + 2* robot_len)*-1, speed=-200),
            GyroPivot(self._robot, -120),
            DriveForward(self._robot, 0.5)
        )
    def Enter(self):
        self._robot.resetOdometry()
    def Update(self):
        if self.command_sequence.update():
            return self.NextState
        else:
            return self.Id