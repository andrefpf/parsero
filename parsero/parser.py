from parsero import syntactic
from parsero.cfg.contextfree_grammar import ContextFreeGrammar
from parsero.common.errors import SyntacticError
from parsero.lexical import LexicalAnalyzer
from parsero.syntactic import ll1_parse


class Parser:
    def __init__(self, regex_path, grammar_path):
        self.lexical = LexicalAnalyzer(regex_path)
        self.cfg = ContextFreeGrammar(grammar_path)
        self.table: dict = syntactic.create_table(self.cfg)

    def parse(self, path: str):
        tokens = self.lexical.tokenize(path)
        ll1_parse(tokens, self.table, self.cfg)
        return "SymbolTable"

    def analyze(self, path: str):
        try:
            self.parse(path)
        except SyntacticError:
            return False
        else:
            return True
