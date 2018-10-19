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
# Possible solutions:
# - Manual state has a pointer to Statemachine and calls its SetState function
# - Manual state has a pointer to a dict of all the possible states and returns one of them from Update
class State():

    def __init__(self, name):
        self.__name = name
        self.__nextState = None
    
    # Name string for this state
    @property
    def Name(self):
        return self.__name

    # A pointer to the next state
    @property
    def NextState(self):
        return self.__nextState

    # Update: Performs actions and returns what the next state should be.
    # Returns self if we should stay in this state.
    def Update(self):
        return self

    # Enter: We call this function once when we enter this state. Any initial
    # actions should be performed here.
    def Enter(self):
        return 0

    # Exit: We call this function once when we leave this state. Any final
    # actions should be performed here.
    def Exit(self):
        return 0