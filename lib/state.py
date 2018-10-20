from enum import Enum

class States(Enum):
    MANUAL = 0
    CHALLENGE1 = 1
    CHALLENGE2 = 2
    CHALLENGE3 = 3
    CHALLENGE4 = 4
    CHALLENGE5 = 5
    CHALLENGE6 = 6

    TRANSIT12 = 12
    TRANSIT23 = 23
    TRANSIT34 = 34
    TRANSIT45 = 45
    TRANSIT56 = 56

# TODO: Each challenge should be a separate class that inherits State
# TODO: Manual state needs to be able to force the state machine into any state.
class State():

    def __init__(self, id, environment):
        self.Id = id
        self.NextState = self.Id
        self._environment = environment
        self._robot = environment["robot"]
        self._sound = self._robot.sound
    
    # Update: Performs actions and returns what the next state should be.
    # Returns self if we should stay in this state.
    def Update(self):
        return self.NextState

    # Enter: We call this function once when we enter this state. Any initial
    # actions should be performed here.
    def Enter(self):
        self._sound.speak("Entering " + self.Id.name)

    # Exit: We call this function once when we leave this state. Any final
    # actions should be performed here.
    def Exit(self):
        self._sound.speak("Exiting " + self.Id.name)