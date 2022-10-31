from parsero import regex
from functools import reduce


class LexicalAnalyzer:
    def __init__(self, regular_definitions_path):
        self.automata = self._generate_automata(regular_definitions_path)
    
    def analyze(self, file):
        pass
    
    def analyze_data(self, data):
        pass
    
    def _generate_automata(self, regular_definitions_path):
        mini_automatas = regex.from_file(regular_definitions_path)
        nd_automata = reduce(or_, mini_automatas.values())
        return nd_automata.determinize()