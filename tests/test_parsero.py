from parsero import Parsero, __version__
from parsero.common.errors import LexicalError, SyntacticError


def test_version():
    assert __version__ == "1.2"


# If a language fails to parse it will raise an error


def test_python():
    parser = Parsero(f"examples/python/python.regex", f"examples/python/python.ghm")
    parser.parse(f"examples/python/example.py")

    try:
        parser.parse(f"examples/c/example.c")
    except LexicalError:
        pass
    except SyntacticError:
        pass
    else:
        # If it can compile wrong language raise error
        assert False


def test_c():
    parser = Parsero(f"examples/c/c.regex", f"examples/c/c.ghm")
    parser.parse(f"examples/c/example.c")

    try:
        parser.parse(f"examples/lisp/example.lisp")
    except LexicalError:
        pass
    except SyntacticError:
        pass
    else:
        # If it can compile wrong language raise error
        assert False


def test_lisp():
    parser = Parsero(f"examples/lisp/lisp.regex", f"examples/lisp/lisp.ghm")
    parser.parse(f"examples/lisp/example.lisp")

    try:
        parser.parse(f"examples/json/example.json")
    except LexicalError:
        pass
    except SyntacticError:
        pass
    else:
        # If it can compile wrong language raise error
        assert False


def test_json():
    parser = Parsero(f"examples/json/json.regex", f"examples/json/json.ghm")
    parser.parse(f"examples/json/example.json")

    try:
        parser.parse(f"examples/python/example.py")
    except LexicalError:
        pass
    except SyntacticError:
        pass
    else:
        # If it can compile wrong language raise error
        assert False
