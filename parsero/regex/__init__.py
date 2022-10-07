from .compile_regex import compile_, from_file


def match(expression: str, string: str) -> int:
    """
    Returns the size of the longest prefix that belongs to the regex language.
    """
    automata = compile_(expression)
    return automata.match(string)


def evaluate(expression: str, string: str) -> bool:
    """
    Checks if the string belongs to the regex language.
    """
    automata = compile_(expression)
    return automata.evaluate(string)
