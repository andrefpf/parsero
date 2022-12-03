from parsero import regex
from parsero.automata import FiniteAutomata, union
from parsero.common.errors import LexicalError
from parsero.common.utils import consume
from parsero.lexical.symbol_table import SymbolTable
from parsero.lexical.token import Token, TokenList


class LexicalAnalyzer:
    def __init__(self, regular_definitions_path):
        self.machine: FiniteAutomata
        self.special_machine: FiniteAutomata
        self.keywords: list
        self._generate_automata(regular_definitions_path)

    def parse(self, path: str) -> tuple[TokenList, SymbolTable]:
        """
        Reads a file and returns the token list and a symbol table
        """

        with open(path) as file:
            string = file.read()
        return self.parse_string(string)

    def parse_string(self, string) -> tuple[TokenList, SymbolTable]:
        """
        Reads a string and returns the token list and a symbol table
        """

        sym_table = SymbolTable()
        tokens = self.tokenize_string(string)

        for word in self.keywords:
            sym_table.insert(word, word)

        for token in tokens:
            if token.name == "id":
                sym_table.insert(token.attribute, token.name)

        return tokens, sym_table

    def analyze(self, path: str) -> bool:
        """
        Checks if a file is accepted by the lexical analyzer.
        """

        try:
            self.tokenize(path)
        except LexicalError:
            return False
        else:
            return True

    def analyze_string(self, string: str) -> bool:
        """
        Checks if a string is accepted by the lexical analyzer.
        """

        try:
            self.tokenize_string(string)
        except LexicalError:
            return False
        else:
            return True

    def tokenize(self, path: str) -> TokenList:
        """
        Create tokens for every lexeme recognized in the file.
        """

        try:
            with open(path) as file:
                return self.tokenize_string(file.read())
        except LexicalError as error:
            error.filename = path
            raise error

    def tokenize_string(self, string: str) -> TokenList:
        """
        Create tokens for every lexeme recognized in the string.
        """

        return TokenList(self.make_tokens(string))

    def make_tokens(self, string: str):
        """
        Generator that yields tokens it finds along a string.
        """

        iterator = enumerate(string)
        line = 1
        col = 1

        for i, char in iterator:
            remaining = string[i:]

            keyword, _ = self.special_machine.match(remaining)
            lexeme, state_index = self.machine.match(remaining)

            if lexeme > keyword:
                consume(len(lexeme) - 1, iterator)
                tag = self.machine.states[state_index].tag
                yield Token(tag, lexeme, i)
                continue
           
            if keyword:
                consume(len(keyword)-1, iterator)
                yield Token(keyword, keyword, i)
                continue

            # it is a bit slow to ignore these chars this far, but
            # languages like python need tokens for identation
            # so we cannot ignore spaces before checking
            # the regular definitions
            if char in " \n\t↳↲":
                continue

            # it should stop before
            msg = f"Invalid expression"
            raise LexicalError.from_data(string, msg, index=i)

    def _generate_automata(self, regular_definitions_path):
        with open(regular_definitions_path) as file:
            machines, keywords = self._read_regular_definitions(file.read())

        special_machines = []
        for word in keywords:
            machine = regex.compiles(word)
            for state in machine.states:
                if state.is_final:
                    state.tag = word
            special_machines.append(machine)

        if machines:
            nd_automata = union(*machines)
            self.machine = nd_automata.determinize()
        else:
            self.machine = FiniteAutomata.empty()

        if special_machines:
            nd_special_automata = union(*special_machines)
            self.special_machine = nd_special_automata.determinize()
        else:
            self.special_machine = FiniteAutomata.empty()

        self.keywords = keywords

    def _read_regular_definitions(self, definitions):
        expressions = dict()
        machines = []
        keywords = []

        tmp_id = []
        for line in definitions.splitlines():
            line = line.strip()
            if not line:
                continue

            line = line.replace("\\n", "\n")

            # support comments
            if line[0] == "#":
                continue

            identifier, expression = line.split(":", 1)  # use only first occurence
            identifier = identifier.strip()
            expression = expression.strip()

            if identifier == expression:
                keywords.append(expression)
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

        return machines, keywords
