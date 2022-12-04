from itertools import cycle

from termcolor import colored

from parsero import syntactic
from parsero.cfg.contextfree_grammar import ContextFreeGrammar
from parsero.common.errors import LexicalError, SyntacticError
from parsero.lexical import LexicalAnalyzer, Token
from parsero.syntactic import (
    calculate_first,
    calculate_follow,
    ll1_parse,
    treat_identation,
)


class Parsero:
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

    def check_ll1(self) -> bool:
        first_dict = calculate_first(self.cfg)
        follow_dict = calculate_follow(self.cfg, first_dict)

        for head, prod in self.cfg.production_rules.items():
            for body in prod:
                if body[0] == "&":
                    intersection = first_dict[head].intersection(follow_dict[head])
                    if intersection:
                        print(head)
                        print(intersection)
                        return False
        return True

    def parse_string(self, string):
        string = treat_identation(string)

        tokens = self.lexical.tokenize_string(string)
        tokens.append(Token("$", "$"))
        # print("TOKENS:")
        # print(tokens)

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
        self.cfg.left_factor()
        self.cfg.refactor_left_recursion()

        self.cfg.refactor_unitary_productions()
        self.cfg.remove_useless_symbols()

        assert self.check_ll1()

    def define_colors(self):
        colors = ["blue", "white", "red", "cyan", "yellow"]
        token_dict = dict()

        for ids in self.lexical.keywords:
            token_dict[ids] = "magenta"

        for ids, color in zip(self.lexical.token_ids, cycle(colors)):
            if "bracket" in ids:
                color = "blue"

            if ids == "comment":
                color = "green"

            token_dict[ids] = color

        return token_dict

    def highlight(self, path):
        separator = "\n" + (100 * "_") + "\n\n"
        token_dict = self.define_colors()
        last_error = None

        with open(path) as file:
            string = file.read()

        string = treat_identation(string)
        remaining = ""

        try:
            self.parse(path)
        except LexicalError as error:
            last_error = error
            remaining = string[error.index :]
            string = string[: error.index]
        except SyntacticError as error:
            last_error = error
            remaining = string[error.index :]
            string = string[: error.index]

        output = []
        last_index = 0
        tokens = self.lexical.tokenize_string(string)
        for token in tokens:
            inter_tokens = string[last_index : token.index]
            lexeme = colored(token.attribute, token_dict[token.name])
            output.append(inter_tokens)
            output.append(lexeme)
            last_index += len(inter_tokens) + len(token.attribute)

        if last_error is not None:
            error_part = colored(remaining, "white", "on_red")
            output.append(error_part)
            output.append(separator)
            output.append(colored(str(last_error), "red"))

        reconstructed = "".join(output)
        return reconstructed
