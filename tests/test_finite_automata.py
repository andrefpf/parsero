from parsero.finite_automata import FiniteAutomata
from parsero.state import State


def test_even_chars():
    """
    L = {w | w bellows to {a, b}* and w is even}
    """

    states = [State("q0", True), State("q1", False)]

    transitions = [
        (0, "a", 1),
        (0, "b", 1),
        (1, "a", 0),
        (1, "b", 0),
    ]

    template = [
        ("aa", True),
        ("aaa", False),
        ("ab", True),
        ("aba", False),
        ("", True),
        ("c", False),
    ]

    automata = FiniteAutomata(states=states, transitions=transitions)

    for string, answer in template:
        assert automata.evaluate(string) == answer
