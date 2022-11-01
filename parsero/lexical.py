from parsero import regex
from parsero.automata import FiniteAutomata
from functools import reduce
from operator import or_
from parsero.utils import consume


class LexicalAnalyzer:
    def __init__(self, regular_definitions_path):
        self.machine: FiniteAutomata
        self.special_machine: FiniteAutomata
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

            special_word, _ = self.special_machine.match(remaining)
            if special_word:
                consume(len(special_word), iterator)
                yield special_word, special_word
                continue
            
            lexeme, state_index = self.machine.match(remaining)
            if lexeme:
                consume(len(lexeme) - 1, iterator)
                tag = self.machine.states[state_index].tag
                yield tag, lexeme  # use Token class
                continue

            spaces, _ = find_spaces.match(remaining)
            if spaces:
                consume(len(spaces) - 1, iterator)
                continue
            
            # se nada der certo
            print(f'\tCaractere desconhecido "{string[i]}"')

    def _generate_automata(self, regular_definitions_path):
        with open(regular_definitions_path) as file:
            machines, special_words = self._read_regular_definitions(file.read())
        
        special_machines = []
        for word in special_words:
            machine = regex.compiles(word)
            for state in machine.states:
                if state.is_final:
                    state.tag = word
            special_machines.append(machine)

        if machines:
            nd_automata = reduce(or_, machines)
            self.machine = nd_automata.determinize()
        else:
            self.machine = FiniteAutomata.empty()

        if special_machines:
            nd_special_automata = reduce(or_, special_machines)
            self.special_machine = nd_special_automata.determinize()
        else:
            self.special_machine = FiniteAutomata.empty()

        self.special_words = special_words

    def _read_regular_definitions(self, definitions):
        expressions = dict()
        machines = []
        special_words = []

        for line in definitions.splitlines():
            line = line.strip()
            if not line:
                continue

            identifier, expression = line.split(":", 1)  # use only first occurence
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