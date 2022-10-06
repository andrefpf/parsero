from .compile_regex import compile_, from_file


def match(expression, string):
    automata = compile_(expression)
    return automata.match(string)


def evaluate(expression, string):
    automata = compile_(expression)
    return automata.evaluate(string)
