from collections import defaultdict
from itertools import count

from parsero.finite_automata import FiniteAutomata
from parsero.regex.regex_tree import anotate_tree, create_regex_tree, calculate_followpos, get_leafs


states_counter = 0


def compile_regex(expression: str) -> FiniteAutomata:
    tree = create_regex_tree(expression)
    tree = anotate_tree(tree)
    followpos = calculate_followpos(tree)

    # dá pra melhorar
    leaf_indexes = defaultdict(set)
    for leaf in get_leafs(tree):
        leaf_indexes[leaf.char] |= leaf.firstpos # or lastpos

    incrementer = count().__next__
    state_index = defaultdict(incrementer)

    alphabet = "ab"
    current_state = frozenset(tree.firstpos)
    index = 0

    for symbol in alphabet:
        u = frozenset()
        for i in current_state.intersection(leaf_indexes[symbol]):
            u |= followpos[i]
        transition = (state_index[current_state], symbol, state_index[u])
        print(transition)