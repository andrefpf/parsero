from parsero import regex
from parsero.automata import FiniteAutomata
from functools import reduce
from operator import or_
from parsero.utils import consume
from parsero.errors import LexicalError


class LexicalAnalyzer:
    def __init__(self, regular_definitions_path):
        self.machine: FiniteAutomata
        self.special_machine: FiniteAutomata
        self.special_words: list
        self._generate_automata(regular_definitions_path)
    
    def analyze(self, path):
        try:
            with open(path) as file:
                self.analyze_data(file.read())
        except LexicalError as e:
            e.filename = path
            raise e
    
    def analyze_data(self, string):
        for tag, lexeme in self.make_tokens(string):
            print(f"<{tag}, {lexeme}>")
        
    def make_tokens(self, string):
        find_spaces = regex.compiles(r"\s+")

        for i, line in enumerate(string.splitlines()):
            iterator = enumerate(line)
            for j, char in iterator:
                remaining = line[j:]

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

                msg = f'Unknown char "{char}"'
                raise LexicalError.from_data(string, msg, line=i+1, col=j+1)


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

        tmp_id = []
        for line in definitions.splitlines():
            line = line.strip()
            if not line:
                continue

            # support comments
            if line[0] == "#":
                continue

            identifier, expression = line.split(":", 1)  # use only first occurence
            identifier = identifier.strip()
            expression = expression.strip()

            if identifier == expression:
                special_words.append(expression)
                continue

            for _id, _exp in expressions.items():
                replaced = expression.replace(_id, _exp)
                if replaced != expression:
                    tmp_id.append(_id)
                    expression = replaced
            expressions[identifier] = expression

        # if an expression is used inside another it doesn't becomes an automata
        for _id in tmp_id:
            expressions.pop(_id)

        for _id, _exp in expressions.items():
            machine = regex.compiles(_exp)
            for state in machine.states:
                if state.is_final:
                    state.tag = _id
            machines.append(machine)
        
        return machines, special_words