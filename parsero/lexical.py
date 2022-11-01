from parsero import regex
from parsero.automata import FiniteAutomata
from functools import reduce
from operator import or_
from parsero.utils import consume


class LexicalAnalyzer:
    def __init__(self, regular_definitions_path):
        self.machine: FiniteAutomata
        self.special_words: list
        self._generate_automata(regular_definitions_path)
    
    def analyze(self, path):
        with open(path) as file:
            self.analyze_data(file.read())
    
    def analyze_data(self, string):
        for i in self.make_tokens(string):
            print(i)
        
    def make_tokens(self, string):
        find_spaces = regex.compiles(r"\s+")
        iterator = iter(range(len(string)))

        for i in iterator:
            remaining = string[i:]
            lexeme, state_index = self.machine.match(remaining)
            spaces, _ = find_spaces.match(remaining)

            if state_index > 0:
                tag = self.machine.states[state_index].tag
                yield tag, lexeme  # use Token class
                consume(len(lexeme) - 1, iterator)
            elif spaces:
                consume(len(spaces) - 1, iterator)
            else:
                print(f'Caractere desconhecido "{string[i]}"')

    def _generate_automata(self, regular_definitions_path):
        with open(regular_definitions_path) as file:
            machines, special_words = self._read_regular_definitions(file.read())
        nd_automata = reduce(or_, machines)
        self.machine = nd_automata.determinize()
        self.special_words = special_words

    def _read_regular_definitions(self, definitions):
        expressions = dict()
        machines = []
        special_words = []

        for line in definitions.splitlines():
            line = line.strip()
            if not line:
                continue

            identifier, expression = line.split(":")
            identifier = identifier.strip()
            expression = expression.strip()

            if identifier == expression:
                special_words.append(expression)
                continue

            for _id, _exp in expressions.items():
                expression = expression.replace(_id, _exp)
            expressions[identifier] = expression

        for _id, _exp in expressions.items():
            machine = regex.compiles(_exp)
            for state in machine.states:
                if state.is_final:
                    state.tag = _id
            machines.append(machine)
        
        return machines, special_words