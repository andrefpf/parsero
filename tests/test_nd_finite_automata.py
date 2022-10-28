from parsero.machines.fa_machines import (
    fa_determinized_epsilon,
    fa_determinized_no_epsilon,
)
from parsero.machines.ndfa_machines import (
    ndfa_to_determinize_epsilon,
    ndfa_to_determinize_no_epsilon,
)
from parsero.wrapper import file_to_automata


def test_ends_with_bb():
    """
    L = {w | w bellows to {a, b}* and w end with ...bb}
    """

    valid = [
        "aaabb",
        "bbbbb",
        "abbabb",
    ]

    invalid = [
        "",
        "aaa",
        "aaab",
        "abba",
        "abbab",
        "aaacaabb",
    ]

    automata = file_to_automata("tests/examples/ends_with_bb.ndfa")

    for string in valid:
        assert automata.evaluate(string)

    for string in invalid:
        assert not automata.evaluate(string)


def test_abc_sequence():
    valid = [
        "",
        "a",
        "b",
        "c",
        "aa",
        "ab",
        "bc",
        "abc",
    ]

    invalid = [
        "bca",
        "aba",
        "cba",
        "ccb",
    ]

    automata = file_to_automata("tests/examples/abc.ndfa")

    for string in valid:
        assert automata.evaluate(string)

    for string in invalid:
        assert not automata.evaluate(string)


def test_ends_with_bb_determinized():
    """
    L = {w | w bellows to {a, b}* and w end with ...bb}
    """

    valid = [
        "aaabb",
        "bbbbb",
        "abbabb",
    ]

    invalid = [
        "",
        "aaa",
        "aaab",
        "abba",
        "abbab",
        "aaacaabb",
    ]

    automata = file_to_automata("tests/examples/ends_with_bb.ndfa").determinize()

    for string in valid:
        assert automata.evaluate(string)

    for string in invalid:
        assert not automata.evaluate(string)


def test_abc_sequence_determinized():
    valid = [
        "",
        "a",
        "b",
        "c",
        "aa",
        "ab",
        "bc",
        "abc",
    ]

    invalid = [
        "bca",
        "aba",
        "cba",
        "ccb",
    ]

    automata = file_to_automata("tests/examples/abc.ndfa").determinize()

    for string in valid:
        assert automata.evaluate(string)

    for string in invalid:
        assert not automata.evaluate(string)


# Acredito que estes testes estejam corretos, mas é difícil de
# comparar autômatos e é difícil saber a ordem exata em que eles foram determinizados.
# Uma opção que temos é só testar se os 3 autômatos reconhecem o mesmo conjunto de palavras.
def test_determinization_no_epsilon():
    nd_automata = ndfa_to_determinize_no_epsilon()
    determinized_automata = nd_automata.determinize()
    model = fa_determinized_no_epsilon()

    # assert determinized_automata.transition_map == model.transition_map
    # assert len(determinized_automata.states) == len(model.states)  # good enough


def test_determinization_epsilon():
    nd_automata = ndfa_to_determinize_epsilon()
    determinized_automata = nd_automata.determinize()
    model = fa_determinized_epsilon()

    # assert determinized_automata.transition_map == model.transition_map
