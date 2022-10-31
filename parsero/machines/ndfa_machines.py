from parsero.automata import NDFiniteAutomata
from parsero.regex.commons import EPSILON
from parsero.automata.state import State


def ndfa_even_chars():
    """
    L = {w | w bellows to {a, b}* and w is even}
    """

    states = [
        State("Even", True),
        State("Odd", False),
    ]

    transitions = [
        (0, "a", 1),
        (0, "b", 1),
        (1, "a", 0),
        (1, "b", 0),
    ]

    return NDFiniteAutomata(states=states, transitions=transitions)


def ndfa_ends_with_bb():
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

    return NDFiniteAutomata(states=states, transitions=transitions)


def ndfa_abc_sequence():
    """
    L = {a^i b^j c^k | i, j, k >= 0}
    """

    states = [
        State("A", True),
        State("B", True),
        State("C", True),
    ]

    transitions = [
        (0, "a", 0),
        (1, "b", 1),
        (2, "c", 2),
        (0, "&", 1),
        (1, "&", 2),
    ]

    return NDFiniteAutomata(states=states, transitions=transitions)


def ndfa_to_determinize_no_epsilon():
    """
    Example 1-1
    https://moodle.ufsc.br/pluginfile.php/5664168/mod_resource/content/6/Resolvidas_Deteminização.pdf
    """

    states = [State("p", False), State("q", True), State("r", False), State("s", True)]

    transitions = [
        (0, "0", {1, 3}),
        (0, "1", 1),
        (1, "0", 2),
        (1, "1", {1, 2}),
        (2, "0", 3),
        (2, "1", 0),
        (3, "1", 0),
    ]

    return NDFiniteAutomata(states=states, transitions=transitions)


def ndfa_to_determinize_epsilon():
    """
    Example 2-1
    https://moodle.ufsc.br/pluginfile.php/5664168/mod_resource/content/6/Resolvidas_Deteminização.pdf
    """
    states = [
        State("p", False),
        State("q", False),
        State("r", True),
    ]

    transitions = [
        (0, EPSILON, {0, 1}),
        (0, "b", 1),
        (0, "c", 2),
        (1, "a", 0),
        (1, "b", 2),
        (1, "c", {0, 1}),
    ]

    return NDFiniteAutomata(states=states, transitions=transitions)
