from lib.state import State, States
from lib.enums import Colors

class StateChallenge1(State):

    def __init__(self, id, environment):
        super().__init__(id, environment)
        self._latestColor = Colors.UNKNOWN

    def Update(self):
        detectedColor = Colors(self._colorSensor.value())
        if detectedColor != self._latestColor:
            print(detectedColor.name)
            self._latestColor = detectedColor
        if detectedColor == Colors.BLUE or detectedColor == Colors.RED:
            self._robot.stop()
            return self.NextState

        if self._ultrasonic.distance_centimeters < 10:
            # turn left if there's something straight ahead
            self._robot.simpleDrive(-100, 100)
        else:
            # Drive straight ahead
            self._robot.driveForwards(500)

        return self.Id

    def Enter(self):
        super().Enter()
        self._colorSensor.mode = 'COL-COLOR'
