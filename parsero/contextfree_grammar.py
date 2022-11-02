class ContextFreeGrammar:
    def __init__(self, productions):
        self.production_rules = self.__create_production_rule(productions)

    def __create_production_rule(self, productions):
        """
        Turns a list of production rules in the format [(symbol, [production]), ..., (symbol, [production])] into a dict
        """

        production_rules = dict()

        for symbol, production in productions:
            production_rules[symbol] = production

        return production_rules
