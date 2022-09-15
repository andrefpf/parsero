from parsero.state import State
from parsero.nd_finite_automata import NDFiniteAutomata
from parsero.finite_automata import FiniteAutomata
from parsero.utils import consume

states = [
    State("initial", False),
    State("is lower case", True),
]

transitions = [
    (0, "a", 1),
    (0, "b", 1),
    (0, "c", 1),
    (0, "d", 1),
    (0, "e", 1),
    (0, "f", 1),
    (0, "g", 1),
    (0, "h", 1),
    (0, "i", 1),
    (0, "j", 1),
    (0, "k", 1),
    (0, "l", 1),
    (0, "m", 1),
    (0, "n", 1),
    (0, "o", 1),
    (0, "p", 1),
    (0, "q", 1),
    (0, "r", 1),
    (0, "s", 1),
    (0, "t", 1),
    (0, "u", 1),
    (0, "v", 1),
    (0, "w", 1),
    (0, "x", 1),
    (0, "y", 1),
    (0, "z", 1),
    (1, "a", 1),
    (1, "b", 1),
    (1, "c", 1),
    (1, "d", 1),
    (1, "e", 1),
    (1, "f", 1),
    (1, "g", 1),
    (1, "h", 1),
    (1, "i", 1),
    (1, "j", 1),
    (1, "k", 1),
    (1, "l", 1),
    (1, "m", 1),
    (1, "n", 1),
    (1, "o", 1),
    (1, "p", 1),
    (1, "q", 1),
    (1, "r", 1),
    (1, "s", 1),
    (1, "t", 1),
    (1, "u", 1),
    (1, "v", 1),
    (1, "w", 1),
    (1, "x", 1),
    (1, "y", 1),
    (1, "z", 1),
]

alphanumericals = FiniteAutomata(states=states, transitions=transitions)


def _find_closing_bracket(string : str) -> int:
    stack = []
    last_closing_bracket = 0
    for i, char in enumerate(string):
        if (char == '(') or (char == '['):
            stack.append(char)
        elif char == ')':
            opening = stack.pop()
            last_closing_bracket = i
            assert opening == '('
        elif char == ']':
            opening = stack.pop()
            last_closing_bracket = i
            assert opening == '['

    if stack:
        raise ValueError("Brackets not matching")

    return i

def compile_regex(string : str) -> NDFiniteAutomata:
    or_operation = False
    # automata = NDFiniteAutomata()

    # remove later
    expression = 'empty'
    
    iterator = enumerate(string)
    for i, char in iterator:
        # read operators
        if char == '*':
            expression = f"({expression})*" 
            # automata = automata.closure()
            continue

        if char == '|':
            or_operation = True
            continue

        # create automata from subexpressions
        if alphanumericals.evaluate(char):
            substring = char
            # consume(iterator, word_size-1)
            # current_automata = _concatenation_automata(substring)
        
        elif char == '(':
            expression_size = _find_closing_bracket(string[i:])
            substring = string[i + 1 : i + expression_size]
            consume(iterator, expression_size)
            current_automata = compile_regex(substring)

        else:
            raise ValueError(f"Unknown symbol {string[i]}")

        # apply operators
        if or_operation:
            expression = f'({expression} | {substring})'
        else:
            expression = f'({expression} + {substring})'
    
    print(expression)
    # return automata
