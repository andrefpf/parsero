from parsero.parser import Parser


def test_python():
    lang = "c"
    parser = Parser(f"examples/{lang}/{lang}.regex", f"examples/{lang}/{lang}.ghm")
    parser.parse(f"examples/{lang}/example.{lang}")