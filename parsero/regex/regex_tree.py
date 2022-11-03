from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional

from treelib import Tree

from parsero.regex.commons import ALPHANUMERIC, EPSILON, SPECIAL, any_blank, any_digit, any_lower_case, any_upper_case
from parsero.utils import consume


class ReNode:
    """
    Base class for regex syntatic tree nodes.

    Operations with higher priority than the node itself must be overloaded.
    """

    def __init__(self):
        self.firstpos = set()
        self.lastpos = set()
        self.nullable = False
        self.grouped = False

    def children(self):
        return []

    def join(self, other):
        return ReUnionNode(self, other)

    def concatenate(self, other):
        return ReConcatNode(self, other)

    def closure(self):
        return ReClosureNode(self)

    def positive_closure(self):
        return ReConcatNode(self, ReClosureNode(self))

    def optional(self):
        """
        Function for the ? operator.
        """
        node = ReUnionNode(ReSymbolNode("&"), self)
        node.grouped = True
        return node

    def _tree_str(self):
        def representation(node):
            if isinstance(node, ReUnionNode):
                return "or"
            elif isinstance(node, ReConcatNode):
                return "."
            elif isinstance(node, ReSymbolNode):
                return node.char
            elif isinstance(node, ReClosureNode):
                return "*"
            else:
                return ""

        tree = Tree()
        stack = [self]

        tree.create_node(representation(self), hash(self))
        while stack:
            node = stack.pop()
            for child in node.children():
                tree.create_node(representation(child), hash(child), parent=hash(node))
                stack.append(child)

        return tree

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return type(self) == type(other) and self.children() == other.children()

    def __str__(self):
        return str(self._tree_str())

    def __iadd__(self, other):
        return self.concatenate(other)

    def __ior__(self, other):
        return self.join(other)


class ReUnionNode(ReNode):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def children(self):
        return [self.left, self.right]

    def concatenate(self, other):
        if self.grouped:
            return ReConcatNode(self, other)
        else:
            self.right = ReConcatNode(self.right, other)
            return self

    def closure(self):
        if self.grouped:
            return ReClosureNode(self)
        else:
            self.right = self.right.closure()
            return self

    def positive_closure(self):
        if self.grouped:
            return ReConcatNode(self, ReClosureNode(self))
        else:
            self.right = self.right.positive_closure()
            return self

    def optional(self):
        if self.grouped:
            node = ReUnionNode(ReSymbolNode("&"), self)
            node.grouped = True
            return node
        else:
            self.right = self.right.optional()
            return self

    def __repr__(self):
        return f"({self.left} | {self.right})"


class ReConcatNode(ReNode):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def children(self):
        return [self.left, self.right]

    def closure(self):
        if self.grouped:
            return ReClosureNode(self)
        else:
            self.right = ReClosureNode(self.right)
            return self

    def positive_closure(self):
        if self.grouped:
            return ReConcatNode(self, ReClosureNode(self))
        else:
            self.right = self.right.positive_closure()
            return self

    def optional(self):
        if self.grouped:
            node = ReUnionNode(ReSymbolNode("&"), self)
            node.grouped = True
            return node
        else:
            self.right = self.right.optional()
            return self

    def __repr__(self):
        return f"({self.left} + {self.right})"


class ReClosureNode(ReNode):
    def __init__(self, child):
        super().__init__()
        self.child = child

    def children(self):
        return [self.child]

    def __repr__(self):
        return f"{self.child}*"


class ReSymbolNode(ReNode):
    def __init__(self, char):
        super().__init__()
        self.char = char

    def __repr__(self):
        return self.char

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return (type(self) == type(other)) and (self.char == other.char)


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


def create_regex_tree(expression: str) -> ReNode:
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
            tree = tree.closure()
            continue
        elif char == "+":
            tree = tree.positive_closure()
            continue
        elif char == "?":
            tree = tree.optional()
            continue

        if char == "\\":  # scaped chars
            _, next_char = next(iterator)
            if next_char == "s":
                subexpression = any_blank
                subtree = create_regex_tree(subexpression)
            elif next_char == "d":
                subexpression = any_digit
                subtree = create_regex_tree(subexpression)
            elif next_char == "w":
                subexpression = f"{any_lower_case}|{any_upper_case}"
                subtree = create_regex_tree(subexpression)
            else:
                subtree = ReSymbolNode(next_char)

        elif char == ".":
            subexpression = f"{any_digit}|{any_lower_case}|{any_upper_case}|{any_blank}"
            subtree = create_regex_tree(subexpression)

        elif char in "([{":
            subexpression = _extract_brackets(expression[i:])
            subtree = create_regex_tree(subexpression)
            length = len(subexpression) + 1
            consume(length, iterator)

        elif (char == EPSILON) or (char in SPECIAL) or (char in ALPHANUMERIC):
            subtree = ReSymbolNode(char)

        else:
            raise ValueError(f'Unknown symbol "{char}"')

        if tree is None:
            tree = subtree
            continue

        # If we have a subtree, we can do some operations
        if join:
            tree |= subtree
            join = False
        else:
            tree += subtree

    tree.grouped = True
    return tree


def anotate_tree(tree: ReNode) -> ReNode:
    # using random utf8 char that no one cares about instead of # sign
    tree = ReConcatNode(tree, ReSymbolNode("⚑"))
    _recursive_anotate_tree(tree, 0)
    return tree


def calculate_followpos(tree: ReNode) -> defaultdict[int, set]:
    followpos = defaultdict(set)
    _recursive_followpos(tree, followpos)
    return followpos


def _recursive_followpos(tree: ReNode, followpos: defaultdict[int, set]):
    if tree is None:
        return

    if isinstance(tree, ReClosureNode):
        for i in tree.lastpos:
            for j in tree.firstpos:
                followpos[i].add(j)
        _recursive_followpos(tree.child, followpos)

    elif isinstance(tree, ReConcatNode):
        for i in tree.left.lastpos:
            for j in tree.right.firstpos:
                followpos[i].add(j)
        _recursive_followpos(tree.left, followpos)
        _recursive_followpos(tree.right, followpos)

    elif isinstance(tree, ReUnionNode):
        _recursive_followpos(tree.left, followpos)
        _recursive_followpos(tree.right, followpos)


def _recursive_anotate_tree(tree: ReNode, tag: int) -> int:
    """
    Recursive function to calculate firstpos and lastpos for all trees.
    """
    if isinstance(tree, ReSymbolNode):
        if tree.char == "&":
            tree.nullable = True
            return tag
        else:
            tree.firstpos = {tag}
            tree.lastpos = {tag}
            tree.nullable = False
            return tag + 1

    if isinstance(tree, ReUnionNode):
        tag = _recursive_anotate_tree(tree.left, tag)
        tag = _recursive_anotate_tree(tree.right, tag)
        tree.firstpos = tree.left.firstpos | tree.right.firstpos
        tree.lastpos = tree.left.lastpos | tree.right.lastpos
        tree.nullable = tree.left.nullable or tree.right.nullable
        return tag

    if isinstance(tree, ReConcatNode):
        tag = _recursive_anotate_tree(tree.left, tag)
        tag = _recursive_anotate_tree(tree.right, tag)

        if tree.left.nullable:
            tree.firstpos = tree.left.firstpos | tree.right.firstpos
        else:
            tree.firstpos = tree.left.firstpos

        if tree.right.nullable:
            tree.lastpos = tree.left.lastpos | tree.right.lastpos
        else:
            tree.lastpos = tree.right.lastpos

        tree.nullable = tree.left.nullable and tree.right.nullable
        return tag

    if isinstance(tree, ReClosureNode):
        tag = _recursive_anotate_tree(tree.child, tag)
        tree.nullable = True
        tree.firstpos = tree.child.firstpos
        tree.lastpos = tree.child.lastpos
        return tag


def get_leafs(tree):
    leafs = []
    if isinstance(tree, (ReUnionNode, ReConcatNode)):
        leafs += get_leafs(tree.left)
        leafs += get_leafs(tree.right)

    elif isinstance(tree, ReClosureNode):
        leafs += get_leafs(tree.child)

    elif isinstance(tree, ReSymbolNode):
        leafs = [tree]

    return leafs
