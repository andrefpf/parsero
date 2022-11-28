from parsero.parser import Parser


def test_python():
    parser = Parser("examples/python.regex", "examples/python.grammar")
    parser.parse("examples/hello_worlds/python.py")