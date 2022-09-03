from parsero.nd_finite_automata import NDFiniteAutomata
from parsero.state import State


def test_even_chars():
    """
    L = {w | w bellows to {a, b}* and w is even}
    """

    states = [State("Even", True), State("Odd", False)]

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

    automata = NDFiniteAutomata(states=states, transitions=transitions)

    for string, answer in template:
        assert automata.evaluate(string) == answer

def test_ends_with_bb():
    """
    L = {w | w bellows to {a, b}* and w end with ...bb}
    """

    states = [
        State("Default", False), 
        State("FirstB", False),
        State("SecondB", True),
    ]

    transitions = [
        (0, "a", 0),
        (0, "b", {0, 1}),
        (1, "b", 2),
        (2, "b", 2),
    ]

    template = [
        ('aaa', False),
        ('aaab', False),
        ('aaabb', True),
        ('bbbbb', True),
        ('abba', False),
        ('abbab', False),
        ('abbabb', True),
        ("", False),
        ("aaacaabb", False),
    ]

    automata = NDFiniteAutomata(states=states, transitions=transitions)

    for string, answer in template:
        assert automata.evaluate(string) == answer
