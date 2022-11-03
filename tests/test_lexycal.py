from parsero.lexical import LexicalAnalyzer
import cProfile

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
    path = "tests/examples/hello_worlds/python.py"
    print(la.analyze(path))
    for token in la.tokenize(path):
        print(token)

def test_cpp():
    la = LexicalAnalyzer("tests/examples/cpp.regex")
    path = "tests/examples/hello_worlds/cpp.cpp"
    print(la.analyze(path))
    for token in la.tokenize(path):
        print(token)

if __name__ == "__main__":
    # cProfile.run("test_python()")
    test_cpp()