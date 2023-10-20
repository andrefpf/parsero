from .compile_regex import *
from .regex_tree import *
from .regex_automata import *
from .compile_regex import compiles


def match(expression: str, string: str) -> int:
    """
    Returns the the longest prefix that belongs to the regex language.
    """
    automata = compiles(expression)
    regex_match = automata.match(string)
    return regex_match.substring


def evaluate(expression: str, string: str) -> bool:
    """
    Checks if the string belongs to the regex language.
    """
    automata = compiles(expression)
    return automata.evaluate(string)
