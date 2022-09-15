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


def _extract_expression(string : str) -> str:
    stack = []
    last_closing_bracket = 0
    for i, char in enumerate(string):
        if (char == '(') or (char == '['):
            stack.append(char)
        elif char == ')':
            opening = stack.pop()
            last_closing_bracket = i
            assert opening == '('
            if not stack:
                break
        elif char == ']':
            opening = stack.pop()
            last_closing_bracket = i
            assert opening == '['
            if not stack:
                break
    else:
        raise ValueError("Brackets not matching")
    
    return string[1:last_closing_bracket]

def debug_infix(op, a, b):
    if (not a) and (not b):
        return ''

    if not a:
        return str(b)

    elif not b:
        return str(a)
    
    else:
        return f'{op}({a}, {b})'

def debug_postfix(op, a):
    if not a:
        return ''
    
    return f'{op}({a})'


def compile_regex(string : str) -> NDFiniteAutomata:
    # expression_automata = NDFiniteAutomata()
    # infix_automata = NDFiniteAutomata()
    # postfix_automata = NDFiniteAutomata()

    postfix_scope = ""
    infix_scope = ""
    expression_scope = ""
    ignore_list = ")]"
    
    iterator = enumerate(string)
    for i, char in iterator:
        if char in ignore_list:
            continue

        if char == '*':
            # postfix_automata = postfix_automata.closure()
            postfix_scope = debug_postfix('closure', postfix_scope)
            continue

        elif char == '+':
            # postfix_automata = postfix_automata.positive_closure()
            postfix_scope = debug_postfix('+closure', postfix_scope)

        elif char == '?':
            # postfix_automata = postfix_automata.any()
            postfix_scope = debug_postfix('any', postfix_scope)
        
        elif alphanumericals.evaluate(char):
            # infix_automata = infix_automata + postfix_automata
            infix_scope = debug_infix('cat', infix_scope, postfix_scope)
            postfix_scope = char
        
        elif char == '(':
            infix_scope = debug_infix('cat', infix_scope, postfix_scope)
            postfix_scope = _extract_expression(string[i:])
            # infix_automata = infix_automata + postfix_automata
            postfix_automata = compile_regex(postfix_scope)
            consume(iterator, len(postfix_scope) + 1)
        
        elif char == '|':
            # infix_automata = infix_automata + postfix_automata
            # expression_automata = expression_automata + infix_automata
            infix_scope = debug_infix('cat', infix_scope, postfix_scope)
            expression_scope = debug_infix('or', expression_scope, infix_scope)
            infix_scope = ""
            postfix_scope = ""

        else:
            raise ValueError(f"Unknown symbol {char}")

    # put together the remaining
    # infix_automata = infix_automata + postfix_automata
    # expression_automata = expression_automata + infix_automata
    infix_scope = debug_infix('cat', infix_scope, postfix_scope)
    expression_scope = debug_infix('or', expression_scope, infix_scope)

    print(expression_scope)
    # return expression_automata
