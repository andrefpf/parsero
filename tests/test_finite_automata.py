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

    automata = file_to_automata("examples/even_chars.fa")

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

    automata = file_to_automata("examples/starts_a_ends_b.fa")

    for string in valid:
        assert automata.evaluate(string)

    for string in invalid:
        assert not automata.evaluate(string)


def test_match():
    automata = file_to_automata("examples/starts_a_ends_b.fa")

    prefix, state = automata.match("abobora")
    assert prefix == "abob"

    prefix, state = automata.match("abroabroaborbarbaorboabraob")
    assert prefix == "abroabroaborbarbaorboabraob"

    prefix, state = automata.match("none")
    assert prefix == ""

    prefix, state = automata.match("ab")
    assert prefix == "ab"
