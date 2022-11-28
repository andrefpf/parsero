from parsero import syntactic
from parsero.contextfree_grammar import ContextFreeGrammar
from parsero.errors import LexicalError, SyntacticError
from parsero.lexical import LexicalAnalyzer
from parsero.syntactic import ll1_parse


class Parser:
    def __init__(self, regex_path, grammar_path):
        self.lexical = LexicalAnalyzer(regex_path)
        self.cfg = ContextFreeGrammar(grammar_path)
        self.table: dict = syntactic.create_table(self.cfg)

    def parse(self, path: str):
        with open(path) as file:
            string = file.read()
        
        try:
            return self.parse_string(string)
        except SyntacticError as error:
            error.filename = path
            raise error
    
    def parse_string(self, string):
        tokens = self.lexical.tokenize_string(string)

        try:
            tree = ll1_parse(tokens, self.table, self.cfg)
        except SyntacticError as error:
            error.data = string
            raise error

    def analyze(self, path: str):
        try:
            self.parse(path)
        except LexicalError:
            return False
        except SyntacticError:
            return False
        else:
            return True
