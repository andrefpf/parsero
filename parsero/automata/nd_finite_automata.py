from functools import cache

from tabulate import tabulate

from parsero import automata
from parsero.automata.state import State
from parsero.common.constants import EPSILON


class NDFiniteAutomata:
    def __init__(self, states, transitions, alphabet, initial_state=0):
        self.states = states
        self.alphabet = alphabet
        self.transition_map = self._create_transition_map(transitions)
        self.initial_state = initial_state

    @classmethod
    def empty(cls):
        return cls(states=[], transitions=[], alphabet=[], initial_state=-1)

    def iterate(self, string):
        """
        Iterates over a string yielding the current states of the automata.
        """

        current_states = self.epsilon_closure(self.initial_state)
        yield current_states

        if not current_states:
            return

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
        for origin in origins:
            if symbol == "&":
                transition = (origin, "\\&")
            else:
                transition = (origin, symbol)
            target |= self.transition_map.get(transition, set())

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

    def union(self, other):
        return automata.union(self, other)

    @cache
    def epsilon_closure(self, state):
        """
        This is a simple DFS algorithm to get all states reachable by epsilon transitions.
        """

        if state == -1:
            return {}

        visited = [False for _ in self.states]
        stack = [state]
        closure = {state}

        visited[state] = True

        while stack:
            s = stack.pop(0)
            epsilon_reachable = self.transition_map.get((s, "&"), [])
            for n in epsilon_reachable:
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

    def _try_add_det_state(self, current_pos, det_states, det_transition_map):
        for symbol in self.alphabet:
            if symbol == EPSILON:
                continue

            if (current_pos, symbol) in det_transition_map:
                continue

            targets = set()
            for pos in current_pos:
                targets |= self.transition_map.get((pos, symbol), set())

            target_pos = set()
            for target in targets:
                target_pos |= self.epsilon_closure(target)
            target_pos = frozenset(target_pos)

            if not target_pos:
                continue

            name = self._get_name_of_state_list(target_pos, self.states)
            is_final = any(self.states[pos].is_final for pos in target_pos)
            tag = ""
            for pos in target_pos:
                if self.states[pos].tag:
                    tag = self.states[pos].tag
                    break
            target_state = State(name, is_final, tag)

            if target_state not in det_states:
                det_states.append(target_state)

            det_transition_map[(current_pos, symbol)] = target_pos
            self._try_add_det_state(target_pos, det_states, det_transition_map)

    def _get_name_of_state_list(self, state_list, states):
        name = ""
        for pos in state_list:
            name += states[pos].name + ","
        return name[:-1]

    def determinize(self) -> automata.FiniteAutomata:
        det_states = []
        det_transition_map = dict()

        state_set = self.epsilon_closure(self.initial_state)
        state_set = frozenset(state_set)
        tag = ""
        for pos in state_set:
            if self.states[pos].tag:
                tag = self.states[pos].tag
                break

        det_states.append(
            State(
                self._get_name_of_state_list(list(state_set), self.states),
                any(self.states[pos].is_final for pos in state_set),
                tag,
            )
        )

        self._try_add_det_state(
            state_set,
            det_states,
            det_transition_map,
        )

        final_transition_map = dict()

        for (origin, symbol), target in det_transition_map.items():
            if isinstance(origin, int):
                origin = (origin,)

            start_name = self._get_name_of_state_list(origin, self.states)
            target_name = self._get_name_of_state_list(list(target), self.states)

            for i in range(len(det_states)):
                if det_states[i].name == start_name:
                    start_index = i
                if det_states[i].name == target_name:
                    target_index = i
            final_transition_map[(start_index, symbol)] = target_index

        alphabet = list(filter(lambda a: a != "&", self.alphabet))
        machine = automata.FiniteAutomata(det_states, [], alphabet, self.initial_state)
        machine.transition_map = final_transition_map
        return machine

    def __or__(self, other):
        return self.union(other)

    def __str__(self):
        headers = ["Q/Σ"] + self.alphabet
        data = []

        for i, state in enumerate(self.states):
            name = '"' + state.name + '"'

            if state.is_final:
                name = "* " + name

            if i == self.initial_state:
                name = "→ " + name

            line = [name]
            for symbol in self.alphabet:
                targets = self.transition_map.get((i, symbol))
                if targets is not None:
                    names = {self.states[i].name for i in targets}
                    line.append(str(names))
                else:
                    line.append("")
            data.append(line)

        return tabulate(data, headers=headers, tablefmt="fancy_grid")
