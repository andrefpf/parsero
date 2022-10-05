from functools import cache


class NDFiniteAutomata:
    def __init__(self, states=None, initial_state=0, transitions=None):
        self.states = states
        self.transition_map = self._create_transition_map(transitions)
        self.initial_state = initial_state

    def travel(self, string):
        """
        Iterates over a string yielding the current states of the automata.
        """
        current_states = self.epsilon_closure(self.initial_state)
        yield current_states

        for symbol in string:
            next_states = set()
            for i in self.compute(current_states, symbol):
                next_states |= self.epsilon_closure(i)
            current_states = next_states

            yield current_states

            if not current_states:
                break

    def compute(self, origins, symbol):
        """
        Executes a single step of computation from origin states through a symbol, then returns the next states.
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
        for states in self.travel(string):
            last_states = states

        for i in last_states:
            if self.states[i].is_final:
                return True
        return False

    @cache
    def epsilon_closure(self, state):
        """
        This is a simple DFS algorithm to get all states reachable by epsilon transitions.
        """

        visited = [False for _ in self.states]
        stack = [state]
        closure = {state}

        visited[state] = True

        while stack:
            s = stack.pop(0)
            for n in self.compute({s}, "&"):
                if not visited[n]:
                    stack.append(n)
                    visited[n] = True
            closure.add(s)
        return closure

    def _create_transition_map(self, transitions):
        """
        Turns a list of transitions in the format [(origin, symbol, states), ..., (origin, symbol, states)] into a dict
        """

        transition_map = dict()
        for origin, symbol, target in transitions:
            if isinstance(target, int):
                transition_map[(origin, symbol)] = {target}
            else:
                transition_map[(origin, symbol)] = set(target)
        return transition_map

    # TODO:Use a lib to print it like a table
    # def __repr__(self):
    #   print("SUS table")
