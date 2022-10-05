from parsero.regex.regex_tree import (
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

    assert tree.symbol == "CONCATENATION"
    assert tree.right.symbol == "#"

    assert tree.left.symbol == "CONCATENATION"
    assert tree.left.right.symbol == "c"

    assert tree.left.left.left.symbol == "CONCATENATION"
    assert tree.left.left.left.left.symbol == "a"
    assert tree.left.left.left.right.symbol == "b"

    assert tree.left.left.right.symbol == "CLOSURE"
    assert tree.left.left.right.left.symbol == "UNION"
    assert tree.left.left.right.left.left.symbol == "a"
    assert tree.left.left.right.left.right.symbol == "b"


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
