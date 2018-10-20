from lib.state import State, States
from lib.enums import Colors

class StateChallenge3(State):

    def __init__(self, id, environment):
        super().__init__(id, environment)
        self._colorSensor = self._robot.colorSensor
        self._leftPushSensor = self._robot.left_push_sensor
        self._rightPushSensor = self._robot.right_push_sensor
        self._lastTurnWasRight = True

    def Update(self):
        detectedColor = self._colorSensor.value()
        if detectedColor == Colors.BLUE or detectedColor == Colors.RED:
            self._robot.stop()
            return self.NextState

        if self._rightPushSensor.is_pressed() and self._leftPushSensor.is_pressed():
            #aja taakse noin 5cm
            if self._lastTurnWasRight:
                #käänny vasemmalle noin 20 astetta
                self._lastTurnWasRight = False
            else:
                #käänny oikealle noin 20 astetta
                self._lastTurnWasRight = True
        elif self._rightPushSensor.is_pressed():
            #aja taakse noin 5cm
            #käänny vasemmalle noin 10 astetta
            pass
        elif self._leftPushSensor.is_pressed():
            #aja taakse noin 5 cm
            #käänny oikealle noin 10 astetta
            pass
        else:
            #aja eteenpäin noin 5 cm
            pass
        return self.Id

    def Enter(self):
        super().Enter()
        self._colorSensor.mode = 'COL-COLOR'