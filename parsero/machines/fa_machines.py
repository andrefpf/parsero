from parsero.finite_automata import FiniteAutomata
from parsero.state import State


def fa_even_chars():
    """
    L = {w | w bellows to {a, b}* and w is even}
    """

    states = [
        State("q0", True),
        State("q1", False),
    ]

    transitions = [
        (0, "a", 1),
        (0, "b", 1),
        (1, "a", 0),
        (1, "b", 0),
    ]

    return FiniteAutomata(states=states, transitions=transitions)


def fa_starts_with_a_ends_with_b():
    """
    L = {w | w bellows to {abor} starts with a and ends with b}
    """

    states = [
        State("q0", False),
        State("q1", False),
        State("q2", True),
    ]

    transitions = [
        (0, "a", 1),
        (1, "a", 1),
        (1, "o", 1),
        (1, "r", 1),
        (1, "b", 2),
        (2, "b", 2),
        (2, "a", 1),
        (2, "o", 1),
        (2, "r", 1),
    ]

    return FiniteAutomata(states=states, transitions=transitions)

