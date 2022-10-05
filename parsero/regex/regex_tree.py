from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional

from parsero.utils import consume


class RegexNode:
    """
    Syntax tree of a regex operation.
    """

    def __init__(self, symbol):
        self.symbol = symbol

        self.left = None
        self.right = None
        self.father = None

        self.firstpos = set()
        self.lastpos = set()
        self.nullable = False

    def set_left(self, node):
        self.left = node
        if node is not None:
            node.father = self
        return self

    def set_right(self, node):
        self.right = node
        if node is not None:
            node.father = self
        return self

    def __repr__(self):
        # TODO: Use a lib to print a nice tree.
        return f"<symbol={self.symbol}>"


def _closure(node: RegexNode) -> RegexNode:
    """
    Add a Kleene Closure node, following the priority of the operators.
    """

    if (node.right is not None) and (node.right.symbol == "#"):
        node.right = None
        node.symbol = "CLOSURE"
        return node
    elif (node.symbol == "CONCATENATION") or (node.symbol == "UNION"):
        tmp = RegexNode("CLOSURE")
        tmp.set_left(node.right)
        node.set_right(tmp)
        return node
    else:
        root = RegexNode("CLOSURE")
        root.set_left(node)
        return root


def _join(node_a: RegexNode, node_b: RegexNode) -> RegexNode:
    """
    Joins two nodes, following the priority of the operators.
    """

    if node_a is None:
        return node_b
    elif node_b is None:
        return node_a

    if (node_a.right is not None) and (node_a.right.symbol == "#"):
        node_a.symbol = "UNION"
        node_a.set_right(node_b)
    else:
        root = RegexNode("UNION")
        root.set_left(node_a)
        root.set_right(node_b)

    return root


def _concat(node_a: RegexNode, node_b: RegexNode) -> RegexNode:
    """
    Concatenates two nodes, following the priority of the operators.
    """
    if node_a is None:
        return node_b
    elif node_b is None:
        return node_a

    # we dont care if the next symbol is a group
    if (node_b.right is not None) and (node_b.right.symbol == "#"):
        node_b = node_b.left

    if node_a.symbol == "UNION":
        tmp = RegexNode("CONCATENATION")
        tmp.set_left(node_a.right)
        tmp.set_right(node_b)
        node_a.set_right(tmp)
        return node_a

    elif (node_a.right is not None) and (node_a.right.symbol == "#"):
        node_a.symbol = "CONCATENATION"
        node_a.set_right(node_b)
        return node_a

    else:
        root = RegexNode("CONCATENATION")
        root.set_left(node_a)
        root.set_right(node_b)
        return root


def _extract_brackets(expression: str) -> str:
    """
    Given an expression starting with some opening bracket ("(", "[", "{")
    finds where the expression is closed and returns the content inside it.

    EXAMPLE:
    >> _extract_brackets("(get [this] part) ignore this")
    get [this] part
    """

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
    """
    Iterates over a regex expression creating a valid syntax tree for it.
    """
    tree = None
    join = False
    iterator = enumerate(expression)

    for i, char in iterator:
        if char == "|":
            join = True  # joins when the second argument appears
            continue
        elif char == "*":
            tree = _closure(tree)
            continue

        if char in "([{":
            subexpression = _extract_brackets(expression[i:])
            subtree = create_regex_tree(subexpression)
            length = len(subexpression) + 1
            consume(length, iterator)
        elif char in "abcd&":  # TODO: char is word/digit
            subtree = RegexNode(char)
        else:
            raise ValueError(f'Unknown symbol "{char}"')

        # If we have a subtree, we can do some operations
        if join:
            tree = _join(tree, subtree)
            join = False
        else:
            tree = _concat(tree, subtree)

    root = RegexNode("CONCATENATION")  # Start of tree symbol
    root.set_left(tree)
    root.set_right(RegexNode("#"))
    return root


def anotate_tree(tree: RegexNode) -> RegexNode:
    _recursive_anotate_tree(tree, 0)
    return tree


def calculate_followpos(tree: RegexNode) -> defaultdict[int, set]:
    followpos = defaultdict(set)
    _recursive_followpos(tree, followpos)
    return followpos


def _recursive_followpos(tree: RegexNode, followpos: defaultdict[int, set]):
    if tree is None:
        return

    if tree.symbol == "CLOSURE":
        for i in tree.lastpos:
            for j in tree.firstpos:
                followpos[i].add(j)

    elif tree.symbol == "CONCATENATION":
        for i in tree.left.lastpos:
            for j in tree.right.firstpos:
                followpos[i].add(j)

    _recursive_followpos(tree.left, followpos)
    _recursive_followpos(tree.right, followpos)


def _recursive_anotate_tree(subtree: RegexNode, index: int) -> int:
    """
    Recursive function to calculate firstpos and lastpos for all subtrees.
    """
    is_leaf = (subtree.left is None) and (subtree.right is None)

    if is_leaf and subtree.symbol == "&":
        subtree.nullable = True
        return index

    if is_leaf and subtree.symbol != "&":
        subtree.firstpos = {index}
        subtree.lastpos = {index}
        subtree.nullable = False
        return index + 1

    if subtree.symbol == "UNION":
        index = _recursive_anotate_tree(subtree.left, index)
        index = _recursive_anotate_tree(subtree.right, index)
        subtree.firstpos = subtree.left.firstpos | subtree.right.firstpos
        subtree.lastpos = subtree.left.lastpos | subtree.right.lastpos
        subtree.nullable = subtree.left.nullable or subtree.right.nullable
        return index

    if subtree.symbol == "CONCATENATION":
        index = _recursive_anotate_tree(subtree.left, index)
        index = _recursive_anotate_tree(subtree.right, index)

        if subtree.left.nullable:
            subtree.firstpos = subtree.left.firstpos | subtree.right.firstpos
        else:
            subtree.firstpos = subtree.left.firstpos

        if subtree.right.nullable:
            subtree.lastpos = subtree.left.lastpos | subtree.right.lastpos
        else:
            subtree.lastpos = subtree.right.lastpos

        subtree.nullable = subtree.left.nullable and subtree.right.nullable
        return index

    if subtree.symbol == "CLOSURE":
        index = _recursive_anotate_tree(subtree.left, index)
        subtree.nullable = True
        subtree.firstpos = subtree.left.firstpos
        subtree.lastpos = subtree.left.lastpos
        return index
