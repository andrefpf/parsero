from parsero.regex import compile_regex


def test_abc_123():
    template = [
        ("a", False),
        ("ab", False),
        ("bc", False),
        ("abcdef", False),
        ("d", False),
        ("de", False),
        ("ef", False),
        ("abc", True),
        ("def", True),
    ]

    automata = compile_regex("a?(a|b)+ab*c")

    # for string, answer in template:
    #     assert automata.evaluate(string) == answer
