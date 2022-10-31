from parsero.automata import file_to_automata


def test_even_chars():
    """
    L = {w | w bellows to {a, b}* and w is even}
    """

    valid = [
        "",
        "aa",
        "ab",
    ]

    invalid = [
        "aaa",
        "aba",
        "c",
    ]

    automata = file_to_automata("tests/examples/even_chars.fa")

    for string in valid:
        assert automata.evaluate(string)

    for string in invalid:
        assert not automata.evaluate(string)


def test_starts_with_a_ends_with_b():
    """
    L = {w | w bellows to {a, b, o, r} starts with a and ends with b}
    """

    valid = [
        "abob",
        "ab",
    ]

    invalid = [
        "a",
        "b",
        "ba",
        "abobora",
    ]

    automata = file_to_automata("tests/examples/starts_a_ends_b.fa")

    for string in valid:
        assert automata.evaluate(string)

    for string in invalid:
        assert not automata.evaluate(string)


def test_match():
    automata = file_to_automata("tests/examples/starts_a_ends_b.fa")

    prefix = automata.match("abobora")
    # abob
    assert prefix == 4

    prefix = automata.match("abroabroaborbarbaorboabraob")
    # whole word
    assert prefix == 27

    prefix = automata.match("none")
    # no matches
    assert prefix == 0

    prefix = automata.match("ab")
    # whole word
    assert prefix == 2
