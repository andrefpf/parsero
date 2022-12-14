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


def test_regex_tree_0():
    tree = create_regex_tree(r"(ab)(a|b)*c")

    template = ReConcatNode(
        ReConcatNode(
            ReConcatNode(ReSymbolNode("a"), ReSymbolNode("b")),
            ReClosureNode(ReUnionNode(ReSymbolNode("a"), ReSymbolNode("b"))),
        ),
        ReSymbolNode("c"),
    )

    assert tree == template


def test_regex_tree_1():
    tree = create_regex_tree(r"a|(bc)*")

    template = ReUnionNode(
        ReSymbolNode("a"), ReClosureNode(ReConcatNode(ReSymbolNode("b"), ReSymbolNode("c")))
    )

    assert tree == template


def test_firstpos_lastpos_followpos():
    tree = create_regex_tree(r"(a|b)*(&|ab)(ab)*(&|a)")
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
