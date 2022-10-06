from parsero.regex.compile_regex import compile_regex, regex_from_file
from parsero.regex.regex_tree import (
    ReClosureNode,
    ReConcatNode,
    ReSymbolNode,
    ReUnionNode,
    _extract_brackets,
    anotate_tree,
    calculate_followpos,
    create_regex_tree,
)


def test_extract_brackets():
    expression = "(hello [world (!)] finish here) ignore this"
    extracted = _extract_brackets(expression)
    assert extracted == "hello [world (!)] finish here"


def test_regex_tree():
    tree = create_regex_tree("(ab)(a|b)*c")

    template = ReConcatNode(
        ReConcatNode(
            ReConcatNode(ReSymbolNode("a"), ReSymbolNode("b")),
            ReClosureNode(ReUnionNode(ReSymbolNode("a"), ReSymbolNode("b"))),
        ),
        ReSymbolNode("c"),
    )

    assert tree == template


def test_firstpos_lastpos_followpos():
    tree = create_regex_tree("(a|b)*(&|ab)(ab)*(&|a)")
    tree = anotate_tree(tree)
    followpos = calculate_followpos(tree)

    assert tree.firstpos == {0, 1, 2, 4, 6, 7}
    assert tree.lastpos == {7}
    assert followpos[0] == {0, 1, 2, 4, 6, 7}
    assert followpos[1] == {0, 1, 2, 4, 6, 7}
    assert followpos[2] == {3}
    assert followpos[3] == {4, 6, 7}
    assert followpos[4] == {5}
    assert followpos[5] == {4, 6, 7}
    assert followpos[6] == {7}
    assert followpos[7] == set()


def test_automata_creation():
    automata = compile_regex("a(a|b)*a|b(a|b)*b|a|b")

    template = [
        ("a", True),
        ("b", True),
        ("aa", True),
        ("bb", True),
        ("aabbababbbbabababa", True),
        ("baabbababbbbababab", True),
        ("ab", False),
        ("ba", False),
        ("abababababab", False),
        ("bababababa", False),
    ]

    for string, answer in template:
        assert automata.evaluate(string) == answer


def test_file_regex():
    automatas = regex_from_file("parsero/machines/example_1.regex")

    assert automatas["digit"].evaluate("2")
    assert automatas["digit"].evaluate("5")
    assert not automatas["digit"].evaluate("81")
    assert not automatas["digit"].evaluate("a")

    assert automatas["letter"].evaluate("a")
    assert automatas["letter"].evaluate("b")
    assert not automatas["letter"].evaluate("oi")
    assert not automatas["letter"].evaluate("5")

    assert automatas["id"].evaluate("banana")
    assert automatas["id"].evaluate("andrezinhogameplay2001")
    assert not automatas["id"].evaluate("007Teste")
    assert not automatas["id"].evaluate("200bananas")
