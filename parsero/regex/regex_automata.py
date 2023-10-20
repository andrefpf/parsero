from parsero.automata import FiniteAutomata, State, DEAD_STATE_INDEX
from dataclasses import dataclass


@dataclass
class RegexMatch:
    substring: str
    state_index: int
    state: State


class RegexAutomata(FiniteAutomata):
    def match(self, string):
        length = 0
        found_state_index = DEAD_STATE_INDEX
        found_state = None

        for i, state_index in enumerate(self.iterate(string)):
            state = self.states[state_index]

            if state_index == DEAD_STATE_INDEX:
                break

            if state.is_final:
                length = i
                found_state_index = state_index
                found_state = state

        return RegexMatch(
            substring=string[:length],
            state_index=found_state_index,
            state=found_state,
        )
