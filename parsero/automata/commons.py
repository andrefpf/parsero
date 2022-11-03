from functools import reduce
from itertools import accumulate
from operator import add

from parsero import automata
from parsero.automata.state import State


def union(*args):
    if len(args) == 0:
        raise ValueError("Union needs at least one argument.")

    alphabets = [m.alphabet for m in args]
    alphabets.append(["&"])
    united_alphabet = list(reduce(add, alphabets))
    united_alphabet = list(set(united_alphabet))  # cringe way to remove duplicates

    united_states = list(reduce(add, [m.states for m in args]))
    united_states.insert(0, State("q0", False))  # new first state

    # rename states
    for i, state in enumerate(united_states):
        state.name = f"q{i}"

    # shift index for every automata in union (plus new initial state)
    shifts = list(accumulate([1] + [len(m.states) for m in args]))

    # shift and join every transition
    united_transitions = []
    for machine, shift in zip(args, shifts):
        if isinstance(machine, automata.NDFiniteAutomata):
            for (origin, symbol), targets in machine.transition_map.items():
                shifted_targets = [target + shift for target in targets]
                transition = (origin + shift, symbol, shifted_targets)
                united_transitions.append(transition)
        else:
            for (origin, symbol), target in machine.transition_map.items():
                transition = (origin + shift, symbol, target + shift)
                united_transitions.append(transition)

    # make an epsilon transition for every initial state of automatas
    initial_transition = (0, "&", [m.initial_state + shift for m, shift in zip(args, shifts)])
    united_transitions.append(initial_transition)
    return automata.NDFiniteAutomata(
        united_states, united_transitions, united_alphabet, initial_state=0
    )
