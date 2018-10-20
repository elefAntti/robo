from lib.state import State, States
from lib.enums import Colors
import RobotInterface

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
            command = RobotInterface.DriveForward(self._robot, -0.05, speed = 200, accuracy = 0.01)
            while not command.update():
                pass
            if self._lastTurnWasRight:
                #käänny vasemmalle noin 20 astetta
                command = RobotInterface.GyroPivot(self._robot, 20, speed = 150, accuracy = 1)
                while not command.update():
                    pass
                self._lastTurnWasRight = False
            else:
                #käänny oikealle noin 20 astetta
                command = RobotInterface.GyroPivot(self._robot, -20, speed = 150, accuracy = 1)
                self._lastTurnWasRight = True
        elif self._rightPushSensor.is_pressed():
            #aja taakse noin 5cm
            command = RobotInterface.DriveForward(self._robot, -0.05, speed = 200, accuracy = 0.01)
            while not command.update():
                pass
            #käänny vasemmalle noin 10 astetta
            command = RobotInterface.GyroPivot(self._robot, 10, speed = 150, accuracy = 1)
            while not command.update():
                pass
        elif self._leftPushSensor.is_pressed():
            #aja taakse noin 5 cm
            command = RobotInterface.DriveForward(self._robot, -0.05, speed = 200, accuracy = 0.01)
            while not command.update():
                pass
            #käänny oikealle noin 10 astetta
            command = RobotInterface.GyroPivot(self._robot, -10, speed = 150, accuracy = 1)
            while not command.update():
                pass
        else:
            #aja eteen noin 10 cm
            command = RobotInterface.DriveForward(self._robot, 0.10, speed = 200, accuracy = 0.01)
            while not command.update():
                pass
        return self.Id

    def Enter(self):
        super().Enter()
        self._colorSensor.mode = 'COL-COLOR'