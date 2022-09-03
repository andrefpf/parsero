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
