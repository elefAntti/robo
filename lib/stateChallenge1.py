from lib.state import State, States
from lib.enums import Colors

class StateChallenge1(State):

    def __init__(self, id, environment):
        super().__init__(id, environment)
        self._robot = environment["robot"]
        self._colorSensor = self._robot.colorSensor

    def Update(self):
        detectedColor = self._colorSensor.value()
        if detectedColor == Colors.BLUE or detectedColor == Colors.RED:
            self._robot.stop()
            return self.NextState

        self._robot.SimpleDrive(500, 500)

        return self.Id

    def Enter(self):
        self._colorSensor.mode = 'COL-COLOR'
