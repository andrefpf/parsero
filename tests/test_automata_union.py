from parsero.automata import file_to_automata, union


def test_dfa_dfa():
    valid = [
        "",
        "aa",
        "ab",
        "abob",
        "ab",
        "ba",
    ]

    invalid = [
        "aaa",
        "aba",
        "c",
        "a",
        "b",
        "abobora",
    ]

    ab = file_to_automata("tests/examples/starts_a_ends_b.fa")
    even = file_to_automata("tests/examples/even_chars.fa")

    automata = ab | even

    for string in valid:
        assert automata.evaluate(string)

    for string in invalid:
        assert not automata.evaluate(string)


def test_ndfa_ndfa():
    valid = [
        "",
        "a",
        "b",
        "c",
        "aa",
        "ab",
        "bc",
        "abc",
        "aaabb",
        "bbbbb",
        "abbabb",
        "aaa",
        "aaab",
        "aaacaabb",
    ]

    invalid = [
        "abba",
        "abbab",
        "bca",
        "aba",
        "cba",
        "ccb",
    ]

    abc = file_to_automata("tests/examples/abc.ndfa")
    bb = file_to_automata("tests/examples/ends_with_bb.ndfa")

    automata = union(abc, bb)
    # automata = abc | bb

    for string in valid:
        assert automata.evaluate(string)

    for string in invalid:
        assert not automata.evaluate(string)
