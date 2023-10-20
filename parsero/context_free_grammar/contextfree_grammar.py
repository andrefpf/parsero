import copy
from collections import defaultdict
from itertools import count

from parsero.common.constants import EPSILON
from parsero.common.errors import SyntacticError


class ContextFreeGrammar:
    def __init__(self, path_to_file):
        all_symbols = set()
        non_terminal_symbols = set()
        productions = list()
        initial_symbol = ""
        self.path_to_file = path_to_file

        with open(path_to_file, "r") as file:
            while line := file.readline():
                line = line.strip()

                if not line:
                    continue

                if line[0] == "#":
                    continue

                production_pieces = line.split("->", 1)
                production_head = production_pieces[0].strip()
                non_terminal_symbols.add(production_head)

                if initial_symbol == "":
                    initial_symbol = production_head

                productions_body = [prod.strip() for prod in production_pieces[1].split("|")]

                production_rule = list()

                for production in productions_body:
                    production = production.split()

                    for symbol in production:
                        all_symbols.add(symbol)

                    production_rule.append(production)

                productions.append((production_head, production_rule))

        terminal_symbols = all_symbols - non_terminal_symbols

        self.non_terminal_symbols = non_terminal_symbols
        self.terminal_symbols = terminal_symbols
        self.initial_symbol = initial_symbol
        self.production_rules = self.__create_production_rule(productions)
        self.original_symbol = dict()

        self.__sort_productions()

    def __create_production_rule(self, productions):
        """
        Turns a list of production rules in the format [(symbol, [production]), ..., (symbol, [production])] into a dict
        """

        production_rules = defaultdict(list)

        for symbol, production in productions:
            production_rules[symbol] = production

        return production_rules

    def __sort_productions(self):
        for productions in self.production_rules.values():
            productions.sort()

    def appears_on_production(self, symbol):
        for productions in self.production_rules.values():
            for production in productions:
                if symbol in production:
                    return True

        return False

    def remove_unreachable_symbols(self):
        reachable_symbols = [self.initial_symbol]
        reachable_terminals = set()

        for reachable_symbol in reachable_symbols:
            for productions in self.production_rules[reachable_symbol]:
                for production in productions:
                    for symbol in productions:
                        if symbol in self.non_terminal_symbols and symbol not in reachable_symbols:
                            reachable_symbols.append(symbol)
                        elif symbol in self.terminal_symbols:
                            reachable_terminals.add(symbol)

        reachable_symbols = set(reachable_symbols)
        symbols_to_remove = self.non_terminal_symbols - reachable_symbols

        for symbol in symbols_to_remove:
            del self.production_rules[symbol]

        self.non_terminal_symbols = self.non_terminal_symbols.intersection(reachable_symbols)
        self.terminal_symbols = self.terminal_symbols.intersection(reachable_terminals)

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

        new_non_terminals = set()
        new_terminals = set()

        for head, body in self.production_rules.items():
            new_non_terminals.add(head)

            for production in body:
                for symbol in production:
                    if symbol in self.terminal_symbols:
                        new_terminals.add(symbol)
                    elif symbol in self.non_terminal_symbols:
                        new_non_terminals.add(symbol)

        self.non_terminal_symbols = new_non_terminals
        self.terminal_symbols = new_terminals

        self.__sort_productions()

    def remove_useless_symbols(self):
        self.remove_unreachable_symbols()
        self.remove_unproductive_symbols()

    def refactor_epsilon_free(self):
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

        if self.initial_symbol in nullable_symbol and self.appears_on_production(
            self.initial_symbol
        ):
            old_initial_symbol = self.initial_symbol
            original_symbol = self.initial_symbol

            if self.initial_symbol in self.original_symbol.keys():
                original_symbol = self.original_symbol[self.initial_symbol]

            z = 0
            while f"{original_symbol}{z}" in self.non_terminal_symbols:
                z += 1

            self.initial_symbol = f"{original_symbol}{z}"
            self.non_terminal_symbols.add(self.initial_symbol)
            self.original_symbol[self.initial_symbol] = original_symbol

            new_production_rules[self.initial_symbol] = [["{}".format(old_initial_symbol)], ["&"]]
        elif self.initial_symbol in nullable_symbol:
            new_production_rules[self.initial_symbol].append(["&"])

        self.production_rules = new_production_rules
        self.__sort_productions()

    def refactor_unitary_productions(self):
        for productions in self.production_rules.values():
            for production in productions:
                if len(production) > 1:
                    continue

                if not production[0] in self.non_terminal_symbols:
                    continue

                new_productions = self.production_rules[production[0]]

                for new_production in new_productions:
                    if new_production not in productions:
                        productions.append(new_production)

        for productions in self.production_rules.values():
            i = 0
            while i < len(productions):
                if len(productions[i]) == 1 and productions[i][0] in self.non_terminal_symbols:
                    productions.pop(i)
                    continue

                i += 1

        self.__sort_productions()

    def refactor_left_recursion(self):
        symbols_to_check = list(self.non_terminal_symbols)
        symbols_to_check.sort()
        symbols_to_check.remove(self.initial_symbol)
        symbols_to_check.insert(0, self.initial_symbol)

        for i in range(len(symbols_to_check)):
            head_symbol = symbols_to_check[i]

            for j in range(i):
                body_symbol = symbols_to_check[j]
                productions = self.production_rules[head_symbol]
                productions_to_adjust = list()

                for production in productions:
                    if production[0] == body_symbol:
                        productions_to_adjust.append(production)

                for production in productions_to_adjust:
                    old_production = production
                    new_productions = list()
                    productions_to_replace_symbol = self.production_rules[body_symbol]
                    production.pop(0)

                    for production_replacement in productions_to_replace_symbol:
                        new_production = list()
                        for symbol in production_replacement:
                            new_production.append(symbol)

                        [new_production.append(symbol) for symbol in production]
                        new_productions.append(new_production)

                    self.production_rules[head_symbol].remove(old_production)
                    [
                        self.production_rules[head_symbol].append(new_production)
                        for new_production in new_productions
                    ]

            original_symbol = head_symbol

            if head_symbol in self.original_symbol.keys():
                original_symbol = self.original_symbol[head_symbol]

            z = 0
            while f"{original_symbol}{z}" in self.non_terminal_symbols:
                z += 1

            left_recursion_symbol = f"{original_symbol}{z}"
            left_recursion_productions = list()

            for production in self.production_rules[head_symbol]:
                if production[0] == head_symbol:
                    left_recursion_productions.append(production)

            if len(left_recursion_productions) > 0:
                self.non_terminal_symbols.add(left_recursion_symbol)
                self.original_symbol[left_recursion_symbol] = original_symbol
                self.terminal_symbols.add("&")
                self.production_rules[left_recursion_symbol].append(["&"])

                for production in self.production_rules[head_symbol]:
                    if production not in left_recursion_productions:
                        production.append(left_recursion_symbol)

            for production in left_recursion_productions:
                self.production_rules[head_symbol].remove(production)

                production.append(left_recursion_symbol)
                production.pop(0)

                self.production_rules[left_recursion_symbol].append(production)

        self.__sort_productions()

    def left_factor(self):
        MAX_SYMBOLS = 1_000

        self.__direct_factoring()

        for i in count():
            old_productions = copy.deepcopy(self.production_rules)
            self.__indirect_factoring()
            self.__direct_factoring()
            if old_productions == self.production_rules:
                break
            elif len(self.non_terminal_symbols) >= MAX_SYMBOLS:
                # Estudantes de computação refutam Turing
                # e resolvem o problema da parada
                msg = f"A gramática o limite durante a fatoração, após {i} iterações."
                raise SyntacticError(self.path_to_file, msg)

        self.__sort_productions()

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
            for start, rest_of_body in symbol_map.items():
                if len(rest_of_body) > 1:
                    original_symbol = head

                    if head in self.original_symbol.keys():
                        original_symbol = self.original_symbol[head]

                    z = 0
                    while f"{original_symbol}{z}" in self.non_terminal_symbols:
                        z += 1
                    new_head = f"{original_symbol}{z}"

                    new_production_rules[new_head] = rest_of_body
                    updated_body.append([start] + [new_head])
                    self.non_terminal_symbols.add(new_head)
                    self.original_symbol[new_head] = original_symbol
                else:
                    if start == EPSILON:
                        all_empty = True
                        non_empty = []
                        for symbol in rest_of_body:
                            if symbol != EPSILON:
                                all_empty = False
                                non_empty.append(symbol)
                        if all_empty:
                            updated_body.append([EPSILON])
                        else:
                            updated_body.append(non_empty[0])
                    else:
                        if rest_of_body[0] == [EPSILON]:
                            rest_of_body[0].pop()
                        rest_of_body[0].insert(0, start)
                        updated_body.append(rest_of_body[0])
            new_production_rules[head] = updated_body
        self.production_rules = new_production_rules

    def __str__(self):
        production_head = list(self.non_terminal_symbols)
        data_partial = list()

        for production in self.production_rules[self.initial_symbol]:
            data_partial.append(" ".join(production))

        data = "{}\t → ".format(self.initial_symbol)
        data += " | ".join(data_partial).strip()

        production_head.remove(self.initial_symbol)
        production_head.sort()

        for symbol in production_head:
            data_partial = list()
            for production in self.production_rules[symbol]:
                data_partial.append(" ".join(production))

            data += "\n"
            data += "{}\t → ".format(symbol)
            data += " | ".join(data_partial).strip()

        return data

    def to_file(self, path_to_file: str):
        data = self.__str__().replace("\t →", " ->")

        with open(path_to_file, "w") as file:
            file.write(data)
