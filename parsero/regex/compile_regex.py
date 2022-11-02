from collections import defaultdict, deque
from itertools import count

from parsero.automata import FiniteAutomata
from parsero.automata.state import State
from parsero.errors import SyntacticError

from parsero.regex.commons import (
    any_blank,
    any_digit,
    any_lower_case,
    any_upper_case,
    any_alphanumeric,
    any_symbol,
)
from parsero.regex.regex_tree import (
    anotate_tree,
    calculate_followpos,
    create_regex_tree,
    get_leafs,
)


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


def _simplify_regex(expression: str) -> str:
    """
    Replace common symbols like \\d for its equivalent syntax (union of all numbers)
    """

    replacement = {
        "[0-9]": f"({any_digit})",
        "[a-z]": f"({any_lower_case})",
        "[A-Z]": f"({any_upper_case})",
        "[a-Z]": f"({any_lower_case}|{any_upper_case})",
        "[a-zA-Z]": f"({any_lower_case}|{any_upper_case})",
    }

    for _id, _exp in replacement.items():
        expression = expression.replace(_id, _exp)
    return expression


def compiles(expression: str) -> FiniteAutomata:
    """
    Converts a regular expression into equivalent Finite Automata.
    """
    expression = _simplify_regex(expression)
    tree = create_regex_tree(expression)

    tree = anotate_tree(tree)
    followpos = calculate_followpos(tree)
    leafs = get_leafs(tree)

    alphabet = [leaf.char for leaf in leafs if leaf.char != "#"]

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

    return FiniteAutomata(
        states=states, transitions=transitions, alphabet=alphabet, initial_state=0
    )


def compile_regular_definitions(definitions: str) -> dict[str, FiniteAutomata]:
    expressions = dict()
    is_identifier = compiles(r"\w(\w|\d|-|_)*")

    for i, line in enumerate(definitions.splitlines(), 1):
        line = line.strip()
        if not line:
            continue

        if ":" not in line:
            msg = 'Regular definitions should be separated by ":".'
            raise SyntacticError.from_data(definitions, msg, line=i)

        identifier, expression = line.split(":")
        identifier = identifier.strip()
        expression = expression.strip()

        if not identifier:
            msg = "The left side of the expression shoud not be empty."
            raise SyntacticError.from_data(definitions, msg, line=i)

        if not expression:
            msg = "The right side of the expression shoud not be empty."
            col = line.index(":") + 1
            raise SyntacticError.from_data(definitions, msg, line=i, col=col)

        recognized, _ = is_identifier.match(identifier)
        col = len(recognized)
        if col < len(identifier):
            msg = "Invalid identifier."
            raise SyntacticError.from_data(definitions, msg, line=i, col=(col + 1))

        for _id, _exp in expressions.items():
            expression = expression.replace(_id, _exp)
        expressions[identifier] = expression

    automatas = dict()

    for _id, _exp in expressions.items():
        automata = compiles(_exp)
        automatas[_id] = automata
        for state in automata.states:
            if state.is_final:
                state.tag = _id

    return automatas


def from_file(path: str) -> dict[str, FiniteAutomata]:
    try:
        with open(path, "r") as file:
            data = file.read()
        return compile_regular_definitions(data)
    except SyntacticError as e:
        e.filename = path
        raise e
