from copy import deepcopy
from parsero import automata

DEAD_STATE = -1


class FiniteAutomata:
    def __init__(self, states, transitions, alphabet, initial_state=0):
        self.states = states
        self.initial_state = initial_state
        self.alphabet = alphabet
        self.transition_map = self._create_transition_map(transitions)

    @classmethod
    def empty(cls):
        return cls(states=[], transitions=[], alphabet=[], initial_state=-1)

    def iterate(self, string):
        """
        Iterates over a string yielding the current state of the automata.
        """
        current_state = self.initial_state
        yield current_state
        if current_state is DEAD_STATE:
            return

        for symbol in string:
            current_state = self.compute(current_state, symbol)
            yield current_state
            if current_state is DEAD_STATE:
                break

    def evaluate(self, string):
        """
        Checks if the string bellows to the automata language.
        """

        for state in self.iterate(string):
            last_state = state

        if last_state == DEAD_STATE:
            return False
        else:
            return self.is_state_final(last_state)

    def is_state_final(self, state):
        return self.states[state].is_final

    def match(self, string):
        """
        Returns a number that corresponds to the length of the longest prefix recognized by the automata.

        If the automata recognizes the language
        L = {w | w bellows to {abor} starts with a and ends with b}

        and your test string is "abobora", this function will return 4, corresponding to the suffix "abob".
        """

        length = 0
        last_recognized_state = DEAD_STATE

        for i, state in enumerate(self.iterate(string)):
            if state == DEAD_STATE:
                break
            if self.is_state_final(state):
                length = i

        return length

    def compute(self, origin, symbol):
        """
        Executes a single step of computation from a origin state through a symbol, then returns the next state.
        """
        try:
            return self.transition_map[(origin, symbol)]
        except KeyError:
            return DEAD_STATE
    
    def union(self, other):
        united_alphabet = list(set(self.alphabet + other.alphabet + ["&"]))  # dumb way to remove repetitions
        united_states = [State("q0", False)] + deepcopy(self.states) + deepcopy(other.states)
        united_transitions = []

        # shift indexes for first and second list of states
        sh0 = 1
        sh1 = sh0 + len(self.states)

        for (origin, symbol), target in self.transition_map.items():
            transition = (origin + sh0, symbol, target + sh0)
            united_transitions.append(transition)

        for (origin, symbol), target in other.transition_map.items():
            transition = (origin + sh1, symbol, target + sh1)
            united_transitions.append(transition)

        initial_transition = (0, "&", (self.initial_state + sh0, other.initial_state + sh1))
        united_transitions.append(initial_transition)
        
        return automata.NDFiniteAutomata(united_states, united_transitions, united_alphabet, initial_state=0)

    def _create_transition_map(self, transitions):
        """
        Turns a list of transitions in the format [(origin, symbol, state), ..., (origin, symbol, state)] into a dict
        """

        transition_map = dict()
        for origin, symbol, target in transitions:
            transition_map[(origin, symbol)] = target
        return transition_map
    
    def __or__(self, other):
        return self.union(other)

    # TODO:Use a lib to print it like a table
    # def __repr__(self):
    #   print("SUS table")
