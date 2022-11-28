from parsero.parser import Parser


def test_python():
    parser = Parser("examples/c/c.regex", "examples/c/c.grammar")
    parser.parse("examples/c/valid_0.c")