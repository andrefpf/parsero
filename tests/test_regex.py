from parsero.regex.regex_tree import _extract_brackets, create_regex_tree


def test_extract_brackets():
    expression = "(hello [world (!)] finish here) ignore this"
    extracted = _extract_brackets(expression)
    assert extracted == "hello [world (!)] finish here"


def test_regex_tree():
    tree = create_regex_tree("ab(a|b)*")

    assert tree.left.symbol == ""
    assert tree.left.left.symbol == "a"
    assert tree.left.right.symbol == "b"

    assert tree.right.symbol == "*"
    assert tree.right.left.symbol == "|"
    assert tree.right.left.left.symbol == "a"
    assert tree.right.left.right.symbol == "b"
