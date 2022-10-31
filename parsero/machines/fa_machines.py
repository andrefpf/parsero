from parsero.finite_automata import FiniteAutomata
from parsero.state import State


def fa_determinized_no_epsilon():
    """
    Example 1-1
    https://moodle.ufsc.br/pluginfile.php/5664168/mod_resource/content/6/Resolvidas_Deteminização.pdf
    """
    states = [
        State("p", False),
        State("q", True),
        State("r", False),
        State("s", True),
        # -----------
        State("q,s", True),
        State("q,r", True),
        State("r,s", True),
        State("p,q,r", True),
        State("q,r,s", True),
    ]

    transitions = [
        (0, "0", 4),
        (0, "1", 1),
        (1, "0", 2),
        (1, "1", 5),
        (2, "0", 3),
        (2, "1", 0),
        (3, "1", 0),
        # -----------
        (4, "0", 2),
        (4, "1", 7),
        (5, "0", 6),
        (5, "1", 7),
        (6, "0", 3),
        (6, "1", 0),
        (7, "0", 8),
        (7, "1", 7),
        (8, "0", 6),
        (8, "1", 7),
    ]

    return FiniteAutomata(states=states, transitions=transitions, alphabet=list("01"))


def fa_determinized_epsilon():
    """
    Example 2-1
    https://moodle.ufsc.br/pluginfile.php/5664168/mod_resource/content/6/Resolvidas_Deteminização.pdf
    """
    states = [State("p,q", False), State("q,r", True), State("p,q,r", True), State("r", True)]

    transitions = [
        # -----------
        (0, "a", 0),
        (0, "b", 1),
        (0, "c", 2),
        (1, "a", 0),
        (1, "b", 3),
        (1, "c", 0),
        (2, "a", 0),
        (2, "b", 1),
        (2, "c", 2),
    ]

    return FiniteAutomata(states=states, transitions=transitions, alphabet=list("01"))
