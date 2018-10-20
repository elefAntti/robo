from lib.state import State, States
from lib.enums import Colors

class LineFollower(State):

    def __init__(self, id, environment):
        super().__init__(id, environment)
        self._robot = environment["robot"]
        self._colorSensor = self._robot.colorSensor
        self._gyro = self._robot.gyro
        self._turn = 200
        self._bright = 15
        self._tspd = -120

    def Update(self):
        print(self._colorSensor.value())        
        rspd = 0
        if self._colorSensor.value() > self._bright:
            rspd = -self._turn
        else:
            rspd = self._turn

        right = (self._tspd + rspd)/2.0
        left = self._tspd - right
        self._robot.SimpleDrive(left, right)

        return self.Id

    def Enter(self):
        self._colorSensor.mode = 'COL-REFLECT'

    def Exit(self):
        self._robot.stop()
