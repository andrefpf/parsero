from parsero.finite_automata import FiniteAutomata
from parsero.state import State


def digit():
    states = [
        State("initial", False),
        State("is digit", True),
    ]

    transitions = [
        (0, "0", 1),
        (0, "1", 1),
        (0, "2", 1),
        (0, "3", 1),
        (0, "4", 1),
        (0, "5", 1),
        (0, "6", 1),
        (0, "7", 1),
        (0, "8", 1),
        (0, "9", 1),
    ]

    return FiniteAutomata(states=states, transitions=transitions)


def lower_case():
    states = [
        State("initial", False),
        State("is lower case", True),
    ]

    transitions = [
        (0, "a", 1),
        (0, "b", 1),
        (0, "c", 1),
        (0, "d", 1),
        (0, "e", 1),
        (0, "f", 1),
        (0, "g", 1),
        (0, "h", 1),
        (0, "i", 1),
        (0, "j", 1),
        (0, "k", 1),
        (0, "l", 1),
        (0, "m", 1),
        (0, "n", 1),
        (0, "o", 1),
        (0, "p", 1),
        (0, "q", 1),
        (0, "r", 1),
        (0, "s", 1),
        (0, "t", 1),
        (0, "u", 1),
        (0, "v", 1),
        (0, "w", 1),
        (0, "x", 1),
        (0, "y", 1),
        (0, "z", 1),
    ]

    return FiniteAutomata(states=states, transitions=transitions)


def upper_case():
    states = [
        State("initial", False),
        State("is upper case", True),
    ]

    transitions = [
        (0, "A", 1),
        (0, "B", 1),
        (0, "C", 1),
        (0, "D", 1),
        (0, "E", 1),
        (0, "F", 1),
        (0, "G", 1),
        (0, "H", 1),
        (0, "I", 1),
        (0, "J", 1),
        (0, "K", 1),
        (0, "L", 1),
        (0, "M", 1),
        (0, "N", 1),
        (0, "O", 1),
        (0, "P", 1),
        (0, "Q", 1),
        (0, "R", 1),
        (0, "S", 1),
        (0, "T", 1),
        (0, "U", 1),
        (0, "V", 1),
        (0, "W", 1),
        (0, "X", 1),
        (0, "Y", 1),
        (0, "Z", 1),
    ]

    return FiniteAutomata(states=states, transitions=transitions)


# def alphanumerical():
#     return lower_case | upper_case | digit


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
        (0, "0", {1, 3}),
        (0, "1", 1),
        (1, "0", 2),
        (1, "1", {1, 2}),
        (2, "0", 3),
        (2, "1", 0),
        (3, "1", 0),
        # -----------
        ({1, 3}, "0", 2),
        ({1, 3}, "1", {0, 1, 2}),
        ({1, 2}, "0", {2, 3}),
        ({1, 2}, "1", {0, 1, 2}),
        ({2, 3}, "0", 3),
        ({2, 3}, "1", 0),
        ({0, 1, 2}, "0", {1, 2, 3}),
        ({0, 1, 2}, "1", {0, 1, 2}),
        ({1, 2, 3}, "0", {2, 3}),
        ({1, 2, 3}, "1", {0, 1, 2}),
    ]

    return FiniteAutomata(states=states, transitions=transitions)

def fa_determinized_epsilon():
    """
    Example 2-1
    https://moodle.ufsc.br/pluginfile.php/5664168/mod_resource/content/6/Resolvidas_Deteminização.pdf
    """
    states = [
        State("p,q", False),
        State("q,r", True),
        State("p,q,r", True),
        State("r", True)
    ]

    transitions = [
        # -----------
        ({0, 1}, "a", {0, 1}),
        ({0, 1}, "b", {1, 2}),
        ({0, 1}, "c", {0, 1, 2}),

        ({1, 2}, "a", {0, 1}),
        ({1, 2}, "b", {2}),
        ({1, 2}, "c", {0, 1}),

        ({0, 1, 2}, "a", {0, 1}),
        ({0, 1, 2}, "b", {1, 2}),
        ({0, 1, 2}, "c", {0, 1, 2}),

    ]

    return FiniteAutomata(states=states, transitions=transitions)
