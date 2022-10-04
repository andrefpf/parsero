from dataclasses import dataclass, field
from typing import Optional

from parsero.utils import consume


@dataclass
class RegexNode:
    symbol: str

    left: Optional["RegexNode"] = None
    right: Optional["RegexNode"] = None
    father: Optional["RegexNode"] = None

    firstpos: set = field(default_factory=set)
    lastpos: set = field(default_factory=set)
    nulable: bool = False


def _closure(node: RegexNode) -> RegexNode:
    root = RegexNode("*")
    root.left = node
    node.father = root
    return root


def _union(node_a: RegexNode, node_b: RegexNode) -> RegexNode:
    if node_a is None:
        return node_b
    elif node_b is None:
        return node_a

    root = RegexNode("|")
    root.left = node_a
    root.right = node_b
    node_a.father = root
    node_b.father = root
    return root


def _concat(node_a: RegexNode, node_b: RegexNode) -> RegexNode:
    if node_a is None:
        return node_b
    elif node_b is None:
        return node_a

    root = RegexNode("")
    root.left = node_a
    root.right = node_b
    node_a.father = root
    node_b.father = root
    return root


def _extract_brackets(expression: str) -> str:
    brackets_pair = {
        "(": ")",
        "[": "]",
        "{": "}",
        # '<' : '>',
    }

    if expression[0] not in brackets_pair.keys():
        raise ValueError("Expression does not start with brackets")

    stack = []  # it is ok to use a list as a stack

    for i, char in enumerate(expression):
        if char in brackets_pair.keys():
            stack.append(char)

        elif char in brackets_pair.values():
            opening = stack.pop()
            closing = brackets_pair[opening]

            if closing != char:
                raise ValueError(f'Bracket "{opening}" does not match "{closing}" ')

            if not stack:
                return expression[1:i]

    raise ValueError("Brackets not matching")


def create_regex_tree(expression: str) -> RegexNode:
    tree = None
    join = False
    iterator = enumerate(expression)

    for i, char in iterator:
        if char == "|":
            join = True
            continue

        if char in "([{":
            subexpression = _extract_brackets(expression[i:])
            length = len(subexpression) + 1
            subtree = create_regex_tree(subexpression)
            consume(length, iterator)
            lookahead = expression[i + length + 1] if (i + length + 1) < len(expression) else ""

        elif char in "abcd":  # TODO: char is word/digit
            subtree = RegexNode(char)
            lookahead = expression[i + 1] if (i + 1) < len(expression) else ""

        else:
            raise ValueError(f'Unknown symbol "{char}"')

        if lookahead == "*":
            subtree = _closure(subtree)
            consume(length, iterator)

        if join:
            tree = _union(tree, subtree)
            join = False
        else:
            tree = _concat(tree, subtree)

    return tree

