# Isso é só um rascunho, não funciona ainda

class Parser:
    def __init__(self, regex_path, grammar_path):
        self.lexical = LexicalAnalyzer(regex_path)
        self.cfg = file_to_contextfree_grammar(grammar_path)
        self.table: dict = syntactic.create_table(cfg)
    
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