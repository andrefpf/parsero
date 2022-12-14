import cProfile
from pathlib import Path

from parsero.lexical.lexical_analyzer import LexicalAnalyzer
from parsero.lexical.token import Token


def test_tokens():
    test = """
        hi
        128
        PLAU
        ABC123
        -1.65e+13
    """

    template = [
        Token("identifier", "hi"),
        Token("number", "128"),
        Token("identifier", "PLAU"),
        Token("identifier", "ABC123"),
        Token("number", "-1.65e+13"),
    ]

    la = LexicalAnalyzer("examples/example_2.regex")
    for token, expected in zip(la.tokenize_string(test), template):
        assert token == expected


def test_python():
    la = LexicalAnalyzer("examples/python.regex")
    path = "examples/hello_worlds/python.py"
    assert la.analyze(path)
    # for token in la.tokenize(path):
    #     print(token)


def test_cpp():
    la = LexicalAnalyzer("examples/cpp.regex")
    path = "examples/hello_worlds/cpp.cpp"
    assert la.analyze(path)
    # for token in la.tokenize(path):
    #     print(token)


def python_exagerado():
    """
    Esse é um teste completamente desnecessário percorrendo todos os arquivos do próprio código fonte.
    Ele não roda todas as vezes porque demora um pouco e pode atrapalhar o desenvolvimento
    caso seja adicionado algum símbolo diferente.
    """
    la = LexicalAnalyzer("examples/python.regex")
    for p in Path("parsero").rglob("*.py"):
        la.tokenize(p)


if __name__ == "__main__":
    cProfile.run("python_exagerado()")
    # test_python()
