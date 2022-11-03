from parsero import regex
from parsero.automata import FiniteAutomata
from functools import reduce
from operator import or_
from parsero.utils import consume
from parsero.errors import LexicalError
from parsero.token import Token, TokenList


class LexicalAnalyzer:
    def __init__(self, regular_definitions_path):
        self.machine: FiniteAutomata
        self.special_machine: FiniteAutomata
        self.special_words: list
        self._generate_automata(regular_definitions_path)
    
    def analyze(self, path):
        try:
            self.tokenize(path)
        except LexicalError:
            return False
        else:
            return True
    
    def analyze_string(self, string):
        try:
            self.tokenize_string(string)
        except LexicalError:
            return False
        else:
            return True
    
    def tokenize(self, path):
        try:
            with open(path) as file:
                return self.tokenize_string(file.read())
        except LexicalError as e:
            e.filename = path
            raise e
    
    def tokenize_string(self, string):
        return TokenList(self.make_tokens(string))
        
    def make_tokens(self, string):
        iterator = enumerate(string)
        line = 1
        col = 1

        for i, char in iterator:
            if char == " ":
                continue
            
            if char == "\n":
                # col = 1
                # line += 1
                continue

            remaining = string[i:]

            special_word, _ = self.special_machine.match(remaining)
            if special_word:
                # new_lines = special_word.count("\n")
                # if new_lines:
                #     col = 1
                #     line += new_lines

                consume(len(special_word), iterator)
                yield Token(special_word, special_word)
                continue

            lexeme, state_index = self.machine.match(remaining)
            if lexeme:
                # new_lines = special_word.count("\n")
                # if new_lines:
                #     col = 1
                #     line += new_lines

                consume(len(lexeme) - 1, iterator)
                tag = self.machine.states[state_index].tag
                yield Token(tag, lexeme)
                continue


            # it should stop before
            msg = f'Unknown char "{char}"'
            raise LexicalError.from_data(string, msg)


        # find_spaces = regex.compiles(r"\s+")
        # for i, line in enumerate(string.splitlines()):
        #     iterator = enumerate(line)
        #     for j, char in iterator:
        #         remaining = line[j:]

        #         special_word, _ = self.special_machine.match(remaining)
        #         if special_word:
        #             consume(len(special_word), iterator)
        #             yield Token(special_word, special_word)
        #             continue
                
        #         lexeme, state_index = self.machine.match(remaining)
        #         if lexeme:
        #             consume(len(lexeme) - 1, iterator)
        #             tag = self.machine.states[state_index].tag
        #             yield Token(tag, lexeme)
        #             continue

        #         spaces, _ = find_spaces.match(remaining)
        #         if spaces:
        #             consume(len(spaces) - 1, iterator)
        #             continue

        #         msg = f'Unknown char "{char}"'
        #         raise LexicalError.from_data(string, msg, line=i+1, col=j+1)


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

            # print(identifier, expression)

            if identifier == expression:
                special_words.append(expression)
                continue

            id_size = lambda x: len(x[0])
            for _id, _exp in sorted(expressions.items(), key=id_size, reverse=True):
                replaced = expression.replace(_id, _exp)
                if replaced != expression:
                    tmp_id.append(_id)
                    expression = replaced
            expressions[identifier] = expression

        # if an expression is used inside another it doesn't becomes an automata
        for _id in tmp_id:
            expressions.pop(_id, None)  # if not found ignore

        for _id, _exp in expressions.items():
            machine = regex.compiles(_exp)
            for state in machine.states:
                if state.is_final:
                    state.tag = _id
            machines.append(machine)
        
        return machines, special_words