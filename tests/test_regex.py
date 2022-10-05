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
from parsero.regex.compile_regex import compile_regex


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
    automata = compile_regex("(a|b)*(&|ab)(ab)*(&|a)")