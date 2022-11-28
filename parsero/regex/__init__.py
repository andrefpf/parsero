from .compile_regex import *
from .compile_regex import compiles
from .regex_tree import *


def match(expression: str, string: str) -> int:
    """
    Returns the the longest prefix that belongs to the regex language.
    """
    automata = compiles(expression)
    substring, state = automata.match(string)
    return substring


def evaluate(expression: str, string: str) -> bool:
    """
    Checks if the string belongs to the regex language.
    """
    automata = compiles(expression)
    return automata.evaluate(string)
