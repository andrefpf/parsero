from collections import defaultdict
from itertools import count

from parsero.finite_automata import FiniteAutomata
from parsero.regex.regex_tree import (
    anotate_tree,
    calculate_followpos,
    create_regex_tree,
    get_leafs,
)
from parsero.state import State


def compile_regex(expression: str) -> FiniteAutomata:
    tree = create_regex_tree(expression)
    tree = anotate_tree(tree)
    followpos = calculate_followpos(tree)

    # dá pra melhorar
    alphabet = ""
    leaf_indexes = defaultdict(set)
    for leaf in get_leafs(tree):
        leaf_indexes[leaf.char] |= leaf.firstpos
        alphabet += leaf.char

    incrementer = count().__next__
    state_index = defaultdict(incrementer)

    tmp_states = [frozenset(tree.firstpos)]
    transitions = []

    while tmp_states:
        current_state = tmp_states.pop()
        for symbol in alphabet:
            u = frozenset()
            for i in current_state.intersection(leaf_indexes[symbol]):
                u |= followpos[i]
            if u not in state_index:
                tmp_states.append(u)
            transition = (state_index[current_state], symbol, state_index[u])
            transitions.append(transition)

    states = [State(f"q{i}", False) for i in range(len(state_index))]

    final_leaf_index = tuple(tree.right.firstpos)[0]
    for k, v in state_index.items():
        if final_leaf_index in k:
            states[v].is_final = True

    return FiniteAutomata(states=states, initial_state=0, transitions=transitions)
