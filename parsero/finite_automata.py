DEAD_STATE = -1


class FiniteAutomata:
    def __init__(self, states=None, initial_state=0, transitions=None):
        self.states = states
        self.transition_map = self._create_transition_map(transitions)
        self.initial_state = initial_state

    def travel(self, string):
        """
        Iterates over a string yielding the current state of the automata.
        """
        current_state = self.initial_state

        for symbol in string:
            current_state = self.compute(current_state, symbol)

            yield current_state
            if current_state is DEAD_STATE:
                break

    def evaluate(self, string):
        """
        Checks if the string bellows to the automata language.
        """

        last_state = self.initial_state
        for state in self.travel(string):
            last_state = state

        if last_state == DEAD_STATE:
            return False
        else:
            return self.states[last_state].is_final

    def compute(self, origin, symbol):
        """
        Executes a single step of computation from a origin state through a symbol, then returns the next state.
        """
        try:
            return self.transition_map[(origin, symbol)]
        except KeyError:
            return DEAD_STATE

    def _create_transition_map(self, transitions):
        """
        Turns a list of transitions in the format [(origin, symbol, state), ..., (origin, symbol, state)] into a dict
        """

        transition_map = dict()
        for origin, symbol, target in transitions:
            transition_map[(origin, symbol)] = target
        return transition_map
