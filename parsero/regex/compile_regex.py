from collections import defaultdict, deque
from itertools import count

from parsero.finite_automata import FiniteAutomata
from parsero.regex.regex_tree import (
    anotate_tree,
    calculate_followpos,
    create_regex_tree,
    get_leafs,
)
from parsero.state import State


def _get_automata_parameters(*, first_tagset, final_leaf_tag, alphabet, followpos, symbol_tags):
    states = []
    transitions = []

    tagset_to_index = defaultdict(count().__next__)  # gives a new index for new elements
    tagset_queue = deque()
    tagset_queue.appendleft(first_tagset)

    while tagset_queue:
        tagset = tagset_queue.pop()

        i = tagset_to_index[tagset]
        is_final = final_leaf_tag in tagset
        states.append(State(f"q{i}", is_final))

        for symbol in alphabet:
            u = frozenset()
            for i in tagset & symbol_tags[symbol]:
                u |= followpos[i]

            if u not in tagset_to_index:
                tagset_queue.appendleft(u)

            transition = (tagset_to_index[tagset], symbol, tagset_to_index[u])
            transitions.append(transition)

    return states, transitions


def compile_regex(expression: str) -> FiniteAutomata:
    tree = create_regex_tree(expression)
    tree = anotate_tree(tree)
    followpos = calculate_followpos(tree)
    leafs = get_leafs(tree)

    alphabet = "".join([leaf.char for leaf in leafs])

    symbol_tags = defaultdict(set)
    for leaf in leafs:
        symbol_tags[leaf.char] |= leaf.firstpos

    states, transitions = _get_automata_parameters(
        first_tagset=frozenset(tree.firstpos),
        final_leaf_tag=tuple(tree.right.firstpos)[0],
        alphabet=alphabet,
        followpos=followpos,
        symbol_tags=symbol_tags,
    )

    return FiniteAutomata(states=states, initial_state=0, transitions=transitions)


def compile_multiple_regex(expressions: str):
    cached_expressions = {
        
    }

    for line in expressions.splitlines():
        line = line.strip()
        if not line:
            continue

        identifier, expression = line.split(":")
        identifier = identifier.strip()
        expression = expression.strip()

        for _id, _exp in cached_expressions:
            expression = expression.replace(_id, _exp)


        print(f"id='{identifier}', regex='{expression}'")

def regex_from_file(path):
    pass