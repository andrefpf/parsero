from parsero.finite_automata import FiniteAutomata
from parsero.regex.regex_tree import create_regex_tree


def followpos(tree) -> dict[int, set]:
    pass


def compile_regex(expression: str) -> FiniteAutomata:
    tree = create_regex_tree(expression)
