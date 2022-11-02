from parsero.lexical import LexicalAnalyzer


test = """
    hi
    128
    PLAU
    ABC123
    1Hello
    (uepa)
"""

def test_python():
    la = LexicalAnalyzer("tests/examples/python.regex")
    la.analyze("parsero/utils.py")
