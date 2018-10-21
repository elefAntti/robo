from lib.state import State, States
from enum import Enum
from lib.RobotInterface import * 

# Challenge 4: Companion Cube
class StateChallenge4(State):

    def __init__(self, id, environment):
        super().__init__(id, environment)
        self._sequence = CommandSequence(
            DriveToAWall(self._robot, speed = 400),
            DriveForward(self._robot, -0.2, speed = -500),
            GyroPivot(self._robot, -90),
            DriveForward(self._robot, 0.40),
            GyroPivot(self._robot, 90),
            DriveForward(self._robot, 2, speed = 500))
    def Enter(self):
        self._sequence.start()
    def Update(self):
        if self._sequence.update():
            self._robot.stop()
        return self.Id
