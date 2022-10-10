from parsero.machines.ndfa_machines import (
    ndfa_abc_sequence,
    ndfa_ends_with_bb,
    ndfa_even_chars,
    ndfa_to_determinize_no_epsilon,
)


def test_even_chars():
    """
    L = {w | w bellows to {a, b}* and w is even}
    """

    template = [
        ("aa", True),
        ("aaa", False),
        ("ab", True),
        ("aba", False),
        ("", True),
        ("c", False),
    ]

    automata = ndfa_even_chars()

    for string, answer in template:
        assert automata.evaluate(string) == answer


def test_ends_with_bb():
    """
    L = {w | w bellows to {a, b}* and w end with ...bb}
    """

    template = [
        ("aaa", False),
        ("aaab", False),
        ("aaabb", True),
        ("bbbbb", True),
        ("abba", False),
        ("abbab", False),
        ("abbabb", True),
        ("", False),
        ("aaacaabb", False),
    ]

    automata = ndfa_ends_with_bb()

    for string, answer in template:
        assert automata.evaluate(string) == answer


def test_abc_sequence():
    template = [
        ("", True),
        ("a", True),
        ("b", True),
        ("c", True),
        ("aa", True),
        ("ab", True),
        ("bc", True),
        ("abc", True),
        ("bca", False),
        ("aba", False),
        ("cba", False),
        ("ccb", False),
    ]

    automata = ndfa_abc_sequence()

    for string, answer in template:
        assert automata.evaluate(string) == answer

def test_determinization():
    automata = ndfa_to_determinize_no_epsilon()
    automata.determinize()

