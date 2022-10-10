from functools import cache
import copy
from parsero.state import State
from parsero.finite_automata import FiniteAutomata

class NDFiniteAutomata:
    def __init__(self, states=None, initial_state=0, transitions=None):
        self.states = states
        self.transition_map = self._create_transition_map(transitions)
        self.initial_state = initial_state

    def iterate(self, string):
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
        for states in self.iterate(string):
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

    def _try_add_det_state(self, states_pos, nd_states, det_states, nd_trasition_map, det_transition_map):
        if len(states_pos) > 1:
            name = ""
            for pos in states_pos:
                name += nd_states[pos].name + ","
            name = name[:-1]
            new_state = State(name, any(nd_states[pos].is_final == True for pos in states_pos))
            if new_state not in det_states:
                det_states.append(new_state)

                transitions_by_symbol = {}
                for pos in states_pos:
                    for key, value in self.transition_map.items():
                        if pos in key:
                            if key[1] in transitions_by_symbol.keys():
                                transitions_by_symbol[key[1]].append(value)
                            else:
                                transitions_by_symbol[key[1]] = [value]

                for key, value in transitions_by_symbol.items():
                    transition_target = set()
                    for target_pos in value:
                        for pos in target_pos:
                            transition_target.add(pos)
                    name_pos_list = []
                    for val1 in value:
                        for val2 in val1:
                            name_pos_list.append(val2)
                    target_index = set(name_pos_list)
                    det_transition_map[(tuple(states_pos), key)] = target_index
                    self._try_add_det_state(target_index, nd_states, det_states, nd_trasition_map, det_transition_map)

    def determinize(self):
        det_states = copy.deepcopy(self.states)
        det_transition_map = copy.deepcopy(self.transition_map)

        for i in range(len(self.states)):
            value = self.epsilon_closure(i)
            self._try_add_det_state(value, self.states, det_states, self.transition_map, det_transition_map)

        for key, value in self.transition_map.items():
            self._try_add_det_state(value, self.states, det_states, self.transition_map, det_transition_map)

        return FiniteAutomata(det_states, 0, det_transition_map, False)
    # TODO:Use a lib to print it like a table
    # def __repr__(self):
    #   print("SUS table")
