from parsero.parser import Parser


def test_python():
    parser = Parser("tests/examples/python.regex", "tests/examples/python.grammar")
    parser.parse("tests/examples/hello_worlds/python.py")