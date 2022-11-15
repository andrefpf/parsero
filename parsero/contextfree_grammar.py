import copy
from collections import defaultdict
from parsero.regex.commons import EPSILON

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

        production_rules = defaultdict(list)

        for symbol, production in productions:
            production_rules[symbol] = production

        return production_rules

    def appears_on_production(self, symbol):
        for productions in self.production_rules.values():
            for production in productions:
                if symbol in production:
                    return True

        return False

    def remove_unreachable_symbols(self):
        reachable_symbols = [self.initial_symbol]

        for reachable_symbol in reachable_symbols:
            for productions in self.production_rules[reachable_symbol]:
                for production in productions:
                    for symbol in productions:
                        if symbol in self.non_terminal_symbols and symbol not in reachable_symbols:
                            reachable_symbols.append(symbol)

        reachable_symbols = set(reachable_symbols)
        symbols_to_remove = self.non_terminal_symbols - reachable_symbols

        for symbol in symbols_to_remove:
            del self.production_rules[symbol]
            self.non_terminal_symbols.remove(symbol)

    def remove_unproductive_symbols(self):
        productive_productions = defaultdict(list)
        productive_symbols = list(self.terminal_symbols)
        symbols_to_check = list(self.non_terminal_symbols)

        while len(symbols_to_check) > 0:
            symbol_to_check = symbols_to_check.pop(0)

            for production in self.production_rules[symbol_to_check]:
                productive = True

                for symbol in production:
                    if symbol not in productive_symbols:
                        productive = False
                        break

                if productive:
                    if symbol_to_check not in productive_symbols:
                        productive_symbols.append(symbol_to_check)

                        [
                            symbols_to_check.append(symbol)
                            for symbol in self.non_terminal_symbols
                            if symbol not in symbols_to_check
                        ]

                    if production not in productive_productions[symbol_to_check]:
                        productive_productions[symbol_to_check].append(production)

        self.production_rules = productive_productions

    def simplify_useless_symbols(self):
        self.remove_unreachable_symbols
        # self.remove_unproductive_symbols
        pass

    def simplify_epsilon_free(self):
        nullable_symbol = list()
        new_production_rules = defaultdict(list)

        for symbol, productions in self.production_rules.items():
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

        if self.initial_symbol in nullable and self.appears_on_production(self.initial_symbol):
            old_initial_symbol = self.initial_symbol
            self.initial_symbol = "{}'".format(old_initial_symbol)
            self.non_terminal_symbols.add(self.initial_symbol)

            new_production_rules[self.initial_symbol] = [["{}".format(old_initial_symbol)], ["&"]]
        else:
            new_production_rules[self.initial_symbol].append(["&"])

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

    def left_factor(self):
        while True:
            old_productions = copy.deepcopy(self.production_rules)
            self.__indirect_factoring()
            self.__direct_factoring()
            if (old_productions == self.production_rules):
                break

    def __indirect_factoring(self):
        for head, body in self.production_rules.items():
            new_body = []
            for prod in body:
                if prod[0] not in self.terminal_symbols:
                    rules = self.production_rules[prod[0]]
                    for rule in rules:
                        new_prod = rule + prod[1:]
                        if new_prod not in new_body:
                            new_body.append(new_prod)
                else:
                    if prod not in new_body:
                        new_body.append(prod)
            if self.production_rules[head] != new_body:
                self.production_rules[head] = new_body

    def __direct_factoring(self):
        new_production_rules = defaultdict()
        for head, body in self.production_rules.items():
            symbol_map = dict()
            for prod in body:
                if prod[0] not in symbol_map:
                    if len(prod[1:]) > 0:
                        symbol_map[prod[0]] = [prod[1:]]
                    else:
                        symbol_map[prod[0]] = [[EPSILON]]
                        self.terminal_symbols.add(EPSILON)
                else:
                    if len(prod[1:]) > 0:
                        symbol_map[prod[0]].append(prod[1:])
                    else:
                        symbol_map[prod[0]].append([EPSILON])
                        self.terminal_symbols.add(EPSILON)

            updated_body = []
            separators = ""
            for start, rest_of_body in symbol_map.items():
                separators += "'"
                if len(rest_of_body) > 1:
                    if head[0] == "<":
                        new_head = head[:2] + separators + head[2:]
                    else:
                        new_head = "<" + head + separators + ">"
                    new_production_rules[new_head] = rest_of_body
                    updated_body.append([start] + [new_head])
                    self.non_terminal_symbols.add(new_head)
                else:
                    if (start == EPSILON):
                        updated_body.append([EPSILON])
                    else:
                        rest_of_body[0].insert(0, start)
                        updated_body.append(rest_of_body[0])
            new_production_rules[head] = updated_body
        self.production_rules = new_production_rules

    def __str__(self):
        data = "{}\t → ".format(self.initial_symbol)
        data_partial = list()

        productions = self.production_rules[self.initial_symbol]
        productions.sort()

        for prod in productions:
            data_partial.append("".join(prod))

        data += " | ".join(data_partial).strip()

        for symbol, productions in self.production_rules.items():
            if symbol == self.initial_symbol:
                continue

            productions.sort()

            data_partial = []
            for prod in productions:
                data_partial.append("".join(prod))

            data += "\n"
            data += "{}\t → ".format(symbol)
            data += " | ".join(data_partial).strip()

        return data
