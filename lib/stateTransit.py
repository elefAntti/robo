from lib.state import State, States
from lib.enums import Colors

# State for driving across challenge transitions (orange bits)
class StateTransit(State):

    def __init__(self, id, environment):
        super().__init__(id, environment)
        self._latestColor = {0, 0, 0}

    def Update(self):
        red = self._colorSensor.value(0)
        green = self._colorSensor.value(1)
        blue = self._colorSensor.value(2)
        detectedColor = {red, green, blue}
        if detectedColor != self._latestColor:
            print("%d %d %d"%(red, green, blue))
            self._latestColor = detectedColor
        if self._onTransitBoard(red, green, blue):
            # All values above 100, probably on the transit board!
            self._robot.driveForwards(100)
        elif self._overTheEdge(red, green, blue):
            # Really low values for all, probably over the edge!
            # TODO: Figure out which way the track curves
            # TODO: Use Antti's drive task to back up a specific distance
            self._robot.simpleDrive(-100, -50)
        else: # if self._onChallengeFloor(red, green, blue):
            # Low values for all, probably over regular floor!
            self._robot.stop()
            return self.NextState
        
        return self.Id

    def _onTransitBoard(self, red, green, blue):
        return red > 100 and green > 100 and blue > 100

    def _overTheEdge(self, red, green, blue):
        return red < 30 and green < 30 and blue < 30

    def _onChallengeFloor(self, red, green, blue):
        return red < 50 and green < 50 and blue < 50

    def Enter(self):
        super().Enter()
        self._colorSensor.mode = 'RGB-RAW'

