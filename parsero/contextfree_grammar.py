class ContextFreeGrammar:
    def __init__(self, productions):
        self.production_rules = self.__create_production_rule(productions)

    def __create_production_rule(self, productions):
        """
        Turns a list of production rules in the format [(symbol, [production]), ..., (symbol, [production])] into a dict
        """

        production_rules = dict()

        for symbol, production in productions:
            if not production_rules:
                self.initial_symbol = symbol

            production_rules[symbol] = production

        return production_rules

    def simplify_epsilon_free(self):
        nullable_symbol = []
        new_production_rules = dict()

        for symbol, productions in self.production_rules.items():
            new_production_rules[symbol] = list()
            for prod in productions:
                if prod == "&":
                    nullable_symbol.append(symbol)
                    continue

                new_production_rules[symbol].append(prod)

        symbols_to_check = list(new_production_rules.keys())

        while len(symbols_to_check) > 0:
            symbol = symbols_to_check.pop(0)
            i = 0
            while i < len(new_production_rules[symbol]):
                prod = new_production_rules[symbol][i]
                for nullable in nullable_symbol:
                    if not nullable in prod:
                        continue

                    new_prod = prod.replace(nullable, "")

                    if new_prod == "" and not symbol in nullable_symbol:
                        nullable_symbol.append(symbol)
                        symbols_to_check.append(symbol)
                    elif not new_prod == "":
                        new_production_rules[symbol].append(new_prod)

                i += 1

        if self.initial_symbol in nullable:
            old_initial_symbol = self.initial_symbol
            self.initial_symbol = "{}'".format(old_initial_symbol)

            new_production_rules[self.initial_symbol] = ["{}".format(old_initial_symbol), "&"]

        # remove duplicates
        for production in new_production_rules.values():
            for prod in production:
                while production.count(prod) > 1:
                    production.remove(prod)

        self.production_rules = new_production_rules
