from parsero import syntactic
from parsero.contextfree_grammar import ContextFreeGrammar
from parsero.errors import LexicalError, SyntacticError
from parsero.lexical import LexicalAnalyzer
from parsero.syntactic import ll1_parse


class Parser:
    def __init__(self, regex_path, grammar_path, adapt=True):
        self.lexical = LexicalAnalyzer(regex_path)
        self.cfg = ContextFreeGrammar(grammar_path)

        if adapt:
            self.adapt_grammar()

        try:
            self.table: dict = syntactic.create_table(self.cfg)
        except RecursionError as error:
            msg = "Não foi possível remover a recursão à esquerda desta gramática."
            raise SyntacticError(grammar_path, msg)

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

        print("TOKENS:")
        print(tokens)

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
    
    def adapt_grammar(self):
        self.cfg.remove_useless_symbols()
        self.cfg.refactor_epsilon_free()
        self.cfg.refactor_unitary_productions()
        self.cfg.refactor_left_recursion()
        self.cfg.left_factor()