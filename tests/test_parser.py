from parsero.parser import Parser


def test_python():
    lang = "python"
    parser = Parser(f"examples/{lang}/{lang}.regex", f"examples/{lang}/{lang}.ghm")
    # parser.parse(f"parsero/parser.py")
    parser.parse(f"examples/{lang}/example.py")