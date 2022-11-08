class ContextFreeGrammar:
    def __init__(self, non_terminal_symbols, terminal_symbols, productions, initial_symbol):
        self.non_terminal_symbols = non_terminal_symbols
        self.terminal_symbols = terminal_symbols
        self.initial_symbol = initial_symbol
        self.production_rules = self.__create_production_rule(productions)

    def __create_production_rule(self, productions):
        """
        Turns a list of production rules in the format [(symbol, [production]), ..., (symbol, [production])] into a dict
        """

        production_rules = dict()

        for symbol, production in productions:
            production_rules[symbol] = production

        return production_rules

    def simplify_epsilon_free(self):
        nullable_symbol = list()
        new_production_rules = dict()

        for symbol, productions in self.production_rules.items():
            new_production_rules[symbol] = list()
            for prod in productions:
                if prod == ["&"]:
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

                    new_prod = prod.copy()
                    new_prod.remove(nullable)

                    # If new nullable symbol, place it in the nullable_symbol list and
                    # recheck every production
                    # else add the new production if it doesn't exist already
                    if new_prod == [] and not symbol in nullable_symbol:
                        nullable_symbol.append(symbol)
                        [
                            symbols_to_check.append(symbol)
                            for symbol in new_production_rules.keys()
                            if symbol not in symbols_to_check
                        ]
                    elif not new_prod == [] and new_prod not in new_production_rules[symbol]:
                        new_production_rules[symbol].append(new_prod)

                i += 1

        if self.initial_symbol in nullable:
            old_initial_symbol = self.initial_symbol
            self.initial_symbol = "{}'".format(old_initial_symbol)
            self.non_terminal_symbols.add(self.initial_symbol)

            new_production_rules[self.initial_symbol] = [["{}".format(old_initial_symbol)], ["&"]]

        self.production_rules = new_production_rules

    def simplify_unitary_productions(self):
        symbols = list(self.production_rules.keys())

        for productions in self.production_rules.values():
            for production in productions:
                if len(production) > 1:
                    continue

                if not production[0] in symbols:
                    continue

                new_productions = self.production_rules[production[0]]

                for new_production in new_productions:
                    if new_production not in productions:
                        productions.append(new_production)

        for productions in self.production_rules.values():
            i = 0
            while i < len(productions):
                if len(productions[i]) > 1:
                    i += 1
                    continue

                if productions[i][0] in symbols:
                    productions.pop(i)
                    continue

                i += 1

    def __str__(self):
        data = "{}\t → ".format(self.initial_symbol)
        data_partial = list()

        productions = self.production_rules[self.initial_symbol]

        for prod in productions:
            data_partial.append(''.join(prod))
                
        data += " | ".join(data_partial).strip()

        for symbol, productions in self.production_rules.items():
            if symbol == self.initial_symbol:
                continue

            data_partial = []
            for prod in productions:
                data_partial.append(''.join(prod))

            data += "\n"
            data += "{}\t → ".format(symbol)
            data += " | ".join(data_partial).strip()

        return data
