from parsero.parser import Parser


def test_python():
    lang = "lisp"
    parser = Parser(f"examples/{lang}/{lang}.regex", f"examples/{lang}/{lang}.ghm")
    parser.parse(f"examples/{lang}/str8ts.{lang}")