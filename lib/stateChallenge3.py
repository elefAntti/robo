from lib.state import State, States
from lib.enums import Colors
from lib.RobotInterface import DriveForward, GyroPivot, CommandSequence

class StateChallenge3(State):

    def __init__(self, id, environment):
        super().__init__(id, environment)
        self._colorSensor = self._robot.colorSensor
        self._leftPushSensor = self._robot.left_push_sensor
        self._rightPushSensor = self._robot.right_push_sensor
        self._lastTurnWasRight = True
        self._command = GyroPivot(self._robot, -20, speed = 150, accuracy = 1)

    def Update(self):
        detectedColor = self._colorSensor.value()
        if detectedColor == Colors.BLUE or detectedColor == Colors.RED:
            self._robot.stop()
            return self.NextState

        if self._command is not None:
            if self._command.update():
                self._command = None
        elif self._rightPushSensor.is_pressed and self._leftPushSensor.is_pressed:
            #aja taakse noin 5cm
            self._command = DriveForward(self._robot, -0.05, speed = -200, accuracy = 0.01)
            if self._lastTurnWasRight:
                #peruuta 5 cm
                #käänny vasemmalle noin 20 astetta
                self._command = CommandSequence(
                    DriveForward(self._robot, -0.10, speed = -200, accuracy = 0.01),
                    GyroPivot(self._robot, 40, speed = 150, accuracy = 1)
                )
            else:
                #peruuta 5 cm
                #käänny oikealle noin 20 astetta
                self._command = CommandSequence(
                    DriveForward(self._robot, -0.10, speed = -200, accuracy = 0.01),
                    GyroPivot(self._robot, -40, speed = 150, accuracy = 1)
                )
        elif self._rightPushSensor.is_pressed:
            #aja taakse noin 5cm
            #käänny noin 10 astetta oikealle
            self._command = CommandSequence(
                DriveForward(self._robot, -0.05, speed = -200, accuracy = 0.01),
                GyroPivot(self._robot, 20, speed = 150, accuracy = 1)
            )
        elif self._leftPushSensor.is_pressed:
            #aja taakse noin 5 cm
            #käänny oikealle noin 10 astetta
            self._command = CommandSequence(
                DriveForward(self._robot, -0.05, speed = -200, accuracy = 0.01),
                GyroPivot(self._robot, -20, speed = 150, accuracy = 1)
            )
        else:
            #aja eteen noin 10 cm
            self._command = DriveForward(self._robot, 0.10, speed = 200, accuracy = 0.01)
        return self.Id

    def Enter(self):
        super().Enter()
        self._colorSensor.mode = 'COL-COLOR'