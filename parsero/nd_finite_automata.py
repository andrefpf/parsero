class NDFiniteAutomata:
    def __init__(self, states=None, initial_state=0, transitions=None):
        self.states = states
        self.transition_map = self._create_transition_map(transitions)
        self.initial_state = initial_state

    def travel(self, string):
        """
        Iterates over a string yielding the current state of the automata.
        """
        current_states = {self.initial_state}

        for symbol in string:
            current_states = self.compute(current_states, symbol)
            yield current_states
            if not current_states:
                break

    def compute(self, origins, symbol):
        """
        Executes a single step of computation from a origin state through a symbol, then returns the next state.
        """

        target = set()
        for state in origins:
            try:
                target |= self.transition_map[(state, symbol)]
            except KeyError:
                continue
        return target

    def evaluate(self, string):
        """
        Checks if the string bellows to the automata language.
        """

        last_states = {self.initial_state}
        for states in self.travel(string):
            last_states = states

        for i in last_states:
            if self.states[i].is_final:
                return True
        return False

    def _create_transition_map(self, transitions):
        """
        Turns a list of transitions in the format [(origin, symbol, state), ..., (origin, symbol, state)] into a dict
        """

        transition_map = dict()
        for origin, symbol, target in transitions:
            if isinstance(target, int):
                transition_map[(origin, symbol)] = {target}
            else:
                transition_map[(origin, symbol)] = set(target)
        return transition_map
