from parsero.example_machines.fa_machines import fa_even_chars


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
