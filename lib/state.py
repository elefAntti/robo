from enum import Enum

class States(Enum):
    MANUAL = 0      # Teleoperation
    CHALLENGE1 = 1  # Challenge 1: Beginning
    CHALLENGE2 = 2  # Challenge 2: Maze
    CHALLENGE3 = 3  # Challenge 3: Pillars
    CHALLENGE4 = 4  # Challenge 4: Companion cube
    CHALLENGE5 = 5  # Challenge 5: Rotating platforms
    CHALLENGE6 = 6  # Challenge 6: Simon Says
    CHALLENGE7 = 7  # Challenge 7: King of the Hill

    TRANSIT12 = 12  # Transit 1-2
    TRANSIT23 = 23  # Transit 2-3
    TRANSIT34 = 34  # Transit 3-4
    TRANSIT45 = 45  # Transit 4-5
    TRANSIT56 = 56  # Transit 5-6
    TRANSIT67 = 67  # Transit 6-7

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