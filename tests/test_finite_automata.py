from parsero.machines.fa_machines import fa_even_chars, fa_starts_with_a_ends_with_b


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

    automata = fa_even_chars()

    for string, answer in template:
        assert automata.evaluate(string) == answer


def test_starts_with_a_ends_with_b():
    """
    L = {w | w bellows to {a, b, o, r} starts with a and ends with b}
    """

    template = [
        ("a", False),
        ("b", False),
        ("ba", False),
        ("abobora", False),
        ("abob", True),
        ("ab", True),
    ]

    automata = fa_starts_with_a_ends_with_b()

    for string, answer in template:
        assert automata.evaluate(string) == answer


def test_match():
    automata = fa_starts_with_a_ends_with_b()

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
    