from parsero.automata import NDFiniteAutomata
from parsero.automata.state import State
from parsero.common.constants import EPSILON


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

    return NDFiniteAutomata(states=states, transitions=transitions, alphabet=list("01"))


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

    return NDFiniteAutomata(states=states, transitions=transitions, alphabet=list("abc"))
