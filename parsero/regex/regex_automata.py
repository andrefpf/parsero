from parsero.automata import FiniteAutomata, State, DEAD_STATE_INDEX
from dataclasses import dataclass


@dataclass
class RegexMatch:
    substring: str
    state_index: int
    state: State


class RegexAutomata(FiniteAutomata):
    @classmethod
    def from_finite_automata(cls, finite_automata):
        return RegexAutomata(
            finite_automata.states,
            finite_automata.transitions,
            finite_automata.alphabet,
            finite_automata.initial_state,
        )

    def match(self, string: str) -> RegexMatch:
        '''
        Finds the longest string of characters accepted by the automata (from the begining of the string).
        '''
        length = 0
        found_state_index = DEAD_STATE_INDEX
        found_state = None

        for i, state_index in enumerate(self.iterate(string)):
            if state_index == DEAD_STATE_INDEX:
                break

            state = self.states[state_index]
            if state.is_final:
                length = i
                found_state_index = state_index
                found_state = state

        return RegexMatch(
            substring=string[:length],
            state_index=found_state_index,
            state=found_state,
        )
