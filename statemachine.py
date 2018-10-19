from lib.state import State, States

class Statemachine():

    states = {}
    stateManual = State(States.MANUAL)
    stateChallenge1 = State(States.CHALLENGE1)
    stateChallenge2 = State(States.CHALLENGE2)
    stateChallenge3 = State(States.CHALLENGE3)
    stateChallenge4 = State(States.CHALLENGE4)
    stateChallenge5 = State(States.CHALLENGE5)
    stateChallenge6 = State(States.CHALLENGE6)
    stateTransit12 = State(States.TRANSIT12)
    stateTransit23 = State(States.TRANSIT23)
    stateTransit34 = State(States.TRANSIT34)
    stateTransit45 = State(States.TRANSIT45)
    stateTransit56 = State(States.TRANSIT56)

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

        self.stateChallenge1.NextState = States.TRANSIT12
        self.stateTransit12.NextState = States.CHALLENGE2
        self.stateChallenge2.NextState = States.TRANSIT23
        self.stateTransit23.NextState = States.CHALLENGE3
        self.stateChallenge3.NextState = States.TRANSIT34
        self.stateTransit34.NextState = States.CHALLENGE4
        self.stateChallenge4.NextState = States.TRANSIT45
        self.stateTransit45.NextState = States.CHALLENGE5
        self.stateChallenge5.NextState = States.TRANSIT56
        self.stateTransit56.NextState = States.CHALLENGE6

        self.currentState = self.stateChallenge1
        self.currentState.Enter()        

    # Base state machine loop. Should be called from e.g. main run loop once per cycle
    def Run(self):
        nextState = self.currentState.Update()

        if nextState != self.currentState.Id:
            self.currentState.Exit()
            self.currentState = self.states[nextState]
            self.currentState.Enter()
    
    # Force the state machine to enter a specific state
    def SetState(self, newState):
        self.currentState = self.states[newState]