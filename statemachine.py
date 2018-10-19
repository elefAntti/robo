from lib.state import State, States

class Statemachine():

    states = {}
    stateManual = State("Manual")
    stateChallenge1 = State("Challenge 1")
    stateChallenge2 = State("Challenge 2")
    stateChallenge3 = State("Challenge 3")
    stateChallenge4 = State("Challenge 4")
    stateChallenge5 = State("Challenge 5")
    stateChallenge6 = State("Challenge 6")
    stateTransit12 = State("Transit 1-2")
    stateTransit23 = State("Transit 2-3")
    stateTransit34 = State("Transit 3-4")
    stateTransit45 = State("Transit 4-5")
    stateTransit56 = State("Transit 5-6")

    def __init__(self):
        self.states[States.MANUAL] = self.stateManual
        self.states[States.CHALLENGE1] = self.stateChallenge1
        self.states[States.CHALLENGE2] = self.stateChallenge2
        self.states[States.CHALLENGE3] = self.stateChallenge3
        self.states[States.CHALLENGE4] = self.stateChallenge4
        self.states[States.CHALLENGE5] = self.stateChallenge5
        self.states[States.CHALLENGE6] = self.stateChallenge6
        self.states[States.TRANSIT12] = self.stateTransit12
        self.states[States.TRANSIT23] = self.stateTransit23
        self.states[States.TRANSIT34] = self.stateTransit34
        self.states[States.TRANSIT45] = self.stateTransit45
        self.states[States.TRANSIT56] = self.stateTransit56

        self.stateChallenge1.NextState = self.stateTransit12
        self.stateTransit12.NextState = self.stateChallenge2
        self.stateChallenge2.NextState = self.stateTransit23
        self.stateTransit23.NextState = self.stateChallenge3
        self.stateChallenge3.NextState = self.stateTransit34
        self.stateTransit34.NextState = self.stateChallenge4
        self.stateChallenge4.NextState = self.stateTransit45
        self.stateTransit45.NextState = self.stateChallenge5
        self.stateChallenge5.NextState = self.stateTransit56
        self.stateTransit56.NextState = self.stateChallenge6

        self.currentState = self.stateChallenge1
        self.currentState.Enter()        

    # Base state machine loop. Should be called from e.g. main run loop once per cycle
    def Run(self):
        nextState = self.currentState.Update()

        if nextState != self.currentState:
            self.currentState.Exit()
            self.currentState = nextState
            self.currentState.Enter()
    
    # Force the state machine to enter a specific state
    def SetState(self, newState):
        self.currentState = self.states[newState]