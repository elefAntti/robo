from lib.state import State, States
from enum import Enum
from lib import RobotInterface

class CCState(Enum):
    FIRST_PART = 1
    SECOND_PART = 2
    THIRD_PART = 3
    FOURTH_PART = 4
    FIFTH_PART = 5

    DONE = 999

# Challenge 4: Companion Cube
class StateChallenge4(State):

    def __init__(self, id, environment):
        super().__init__(id, environment)
        self._substate = CCState.FIRST_PART

    def Update(self):
        if self._substate == CCState.FIRST_PART:
            # 1. Drive until a wall is detected
            if self._ultrasonic.value() < 100:
                self._pivot = RobotInterface.GyroPivot(self._robot, -90)
                self._substate = CCState.SECOND_PART
            else:
                self._robot.driveForwards(500)
        elif self._substate == CCState.SECOND_PART:
            # 2. Rotate 90 degrees
            if self._pivot.update() == True:
                self._forwardDrive = RobotInterface.DriveForward(self._robot, 40)
                self._substate = CCState.THIRD_PART
        elif self._substate == CCState.THIRD_PART:
            # 3. Drive forwards a little bit
            if self._forwardDrive.update() == True:
                self._pivot = RobotInterface.GyroPivot(self._robot, 90)
                self._substate = CCState.FOURTH_PART
        elif self._substate == CCState.FOURTH_PART:
            # 4. Rotate 90 degrees in the other direction
            if self._pivot.update() == True:
                self._forwardDrive = RobotInterface.DriveForward(self._robot, 1, 500)
                self._substate = CCState.FIFTH_PART
        elif self._substate == CCState.FIFTH_PART:
            # 5. Drive roughly to the button
            if self._forwardDrive.update() == True:
                self._substate = CCState.DONE
                print("No more autonomous movements. Switch to teleop!")
        # else Do nothing

        return self.Id
