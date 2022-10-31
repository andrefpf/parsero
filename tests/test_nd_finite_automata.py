from parsero.automata import file_to_automata
from parsero.machines.fa_machines import (
    fa_determinized_epsilon,
    fa_determinized_no_epsilon,
)
from parsero.machines.ndfa_machines import (
    ndfa_abc_sequence,
    ndfa_ends_with_bb,
    ndfa_even_chars,
    ndfa_to_determinize_epsilon,
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

    automata = file_to_automata("tests/examples/even_chars.ndfa")

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

    automata = file_to_automata("tests/examples/ends_with_bb.ndfa")

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

    automata = file_to_automata("tests/examples/abc.ndfa")

    for string, answer in template:
        assert automata.evaluate(string) == answer


def test_determinization_no_epsilon():
    nd_automata = ndfa_to_determinize_no_epsilon()
    determinized_automata = nd_automata.determinize()
    model = fa_determinized_no_epsilon()
    assert determinized_automata.transition_map == model.transition_map
    assert len(determinized_automata.states) == len(model.states)  # good enough


def test_determinization_epsilon():
    nd_automata = ndfa_to_determinize_epsilon()
    determinized_automata = nd_automata.determinize()
    model = fa_determinized_epsilon()
    assert determinized_automata.transition_map == model.transition_map
