from lib.state import State, States

class Statemachine:
    def __init__(self, environment):
        self.states = {}
        self.stateManual = State(States.MANUAL, environment)
        self.stateChallenge1 = State(States.CHALLENGE1, environment)
        self.stateChallenge2 = State(States.CHALLENGE2, environment)
        self.stateChallenge3 = State(States.CHALLENGE3, environment)
        self.stateChallenge4 = State(States.CHALLENGE4, environment)
        self.stateChallenge5 = State(States.CHALLENGE5, environment)
        self.stateChallenge6 = State(States.CHALLENGE6, environment)
        self.stateTransit12 = State(States.TRANSIT12, environment)
        self.stateTransit23 = State(States.TRANSIT23, environment)
        self.stateTransit34 = State(States.TRANSIT34, environment)
        self.stateTransit45 = State(States.TRANSIT45, environment)
        self.stateTransit56 = State(States.TRANSIT56, environment)

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