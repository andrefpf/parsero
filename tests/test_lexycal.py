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
    path = "parsero/utils.py"
    print(la.analyze(path))
    for token in la.tokenize(path):
        print(token)
