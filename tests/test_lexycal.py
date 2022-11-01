from parsero.lexical import LexicalAnalyzer


test = """
    hi
    128
    PLAU
    ABC123
    1Hello
    (uepa)
"""

# def test_example_1():
#     la = LexicalAnalyzer("tests/examples/example_1.regex")
#     la.analyze_data(test)

def test_python():
    la = LexicalAnalyzer("tests/examples/python.regex")
    la.analyze("parsero/utils.py")
