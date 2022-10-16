from functools import cache
from parsero.state import State
from parsero.finite_automata import FiniteAutomata
from parsero.regex.commons import EPSILON
import copy

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
        transitions_by_symbol = {}

        for pos in states_pos:
            for key, value in self.transition_map.items():
                if pos in key:
                    if key[1] in transitions_by_symbol.keys():
                        transitions_by_symbol[key[1]].append(value)
                    else:
                        transitions_by_symbol[key[1]] = [value]

        for symbol, value in transitions_by_symbol.items():
            if symbol != EPSILON:
                transition_target = set()
                for target_pos in value:
                    for pos in target_pos:
                        transition_target.add(pos)
                name_pos_list = []
                for val1 in value:
                    for val2 in val1:
                        name_pos_list.append(val2)
                target_pos = set(name_pos_list)

                if len(states_pos) > 1:
                    current = (tuple(states_pos))
                else:
                    current = list(states_pos)[0]

                if len(target_pos) > 1:
                    name = self._get_name_of_state_list(target_pos)
                    target_state = State(name, any(nd_states[pos].is_final == True for pos in target_pos))
                else:
                    target_state = State(nd_states[list(target_pos)[0]].name, nd_states[list(target_pos)[0]].is_final)
                if target_state not in det_states:
                    det_states.append(target_state)
                if (current, symbol) not in det_transition_map:
                    det_transition_map[(current, symbol)] = target_pos
                    self._try_add_det_state(target_pos, nd_states, det_states, nd_trasition_map, det_transition_map)

        #
        # for key, value in transitions_by_symbol.items():
        #     self._try_add_det_state(target_pos, nd_states, det_states, nd_trasition_map, det_transition_map)

        # for key, value in transitions_by_symbol.items():
        #     if key != EPSILON:
        #         transition_target = set()
        #         for target_pos in value:
        #             for pos in target_pos:
        #                 transition_target.add(pos)
        #         name_pos_list = []
        #         for val1 in value:
        #             for val2 in val1:
        #                 name_pos_list.append(val2)
        #         target_index = set(name_pos_list)
        #
        #         det_transition_map[(current, key)] = target_index
        #         self._try_add_det_state(target_index, nd_states, det_states, nd_trasition_map, det_transition_map)

    def _get_name_of_state_list(self, state_list):
        name = ""
        for pos in state_list:
            name += self.states[pos].name + ","
        return name[:-1]

    def determinize(self) -> FiniteAutomata:
        det_states = copy.deepcopy(self.states)
        det_transition_map = dict()

        if self.epsilon_closure(self.initial_state) == {self.initial_state}:
            initial_state = self.initial_state
            self._try_add_det_state(self.epsilon_closure(self.initial_state), self.states, det_states, self.transition_map, det_transition_map)

        else:
            initial_closure = list(self.epsilon_closure(self.initial_state))
            name = self._get_name_of_state_list(initial_closure)
            det_states.append(State(name, any(self.states[pos].is_final == True for pos in initial_closure)))
            initial_state = len(det_states) - 1
            self._try_add_det_state(initial_closure, self.states, det_states, self.transition_map, det_transition_map)

        # for key, value in self.transition_map.items():
        #     if (len(value)) == 1:
        #         state = self.states[list(value)[0]]
        #         if state not in det_states:
        #             det_states.append(state)


        # if self.states[initial_state] not in det_states:
        #     det_states.append(self.states[self.initial_state])

        return FiniteAutomata(det_states, initial_state, det_transition_map, False)

    # TODO:Use a lib to print it like a table
    # def __repr__(self):
    #   print("SUS table")
