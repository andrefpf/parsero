from parsero.cfg.contextfree_grammar import ContextFreeGrammar
from parsero.lexical.token import Token
from parsero.common.errors import SyntacticError


def first(head: str, cfg: ContextFreeGrammar) -> set:
    first_set = set()
    if head in cfg.non_terminal_symbols:
        for prod in cfg.production_rules[head]:
            for i in range(len(prod)):
                nullable = False
                if prod[i] in cfg.terminal_symbols:
                    first_set.add(prod[i])
                    break
                else:
                    first_non_terminal = list(first(prod[i], cfg))
                    for symbol in first_non_terminal:
                        if symbol != "&":
                            first_set.add(symbol)
                        else:
                            nullable = True
                    if not nullable:
                        break
            if nullable:
                first_set.add("&")
    else:
        first_set.add(head)
    return first_set


def follow(cfg: ContextFreeGrammar) -> dict:
    follow_dict = dict()
    for head in cfg.production_rules:
        follow_dict[head] = set()

    follow_dict[cfg.initial_symbol].add("$")

    for head, prod in cfg.production_rules.items():
        for body in prod:
            for i in range(len(body)):
                if body[i] in cfg.non_terminal_symbols:
                    if i != len(body) - 1:
                        nullable = False
                        for j in range(i, len(body)):
                            if j != len(body) - 1:
                                first_of_next = first(body[j + 1], cfg)

                                if "&" in first_of_next:
                                    first_of_next.remove("&")
                                    nullable = True
                                    follow_dict[body[i]].update(first_of_next)
                                else:
                                    follow_dict[body[i]].update(first_of_next)
                                    nullable = False
                                    break
                            else:
                                if nullable:
                                    follow_dict[body[i]].update(follow_dict[head])
                    else:
                        if body[i] in cfg.non_terminal_symbols:
                            follow_dict[body[i]].update(follow_dict[head])
    return follow_dict


def create_table(cfg: ContextFreeGrammar) -> dict:
    table = dict()
    follow_dict: dict = follow(cfg)

    for head, prod in cfg.production_rules.items():
        for body in prod:
            first_set = first(body[0], cfg)
            if "&" in first_set:
                first_set.remove("&")
                for symbol in follow_dict[head]:
                    table[(head, symbol)] = body
            for symbol in first_set:
                table[(head, symbol)] = body

    return table


def ll1_parse(tokens: list, table: dict, cfg: ContextFreeGrammar) -> bool:
    stack = ["$", cfg.initial_symbol]

    for token in tokens:
        symbol = token.name
        ready_for_next = False
        while not ready_for_next:
            current = stack.pop()

            if symbol == current:
                ready_for_next = True
                continue

            if not (current, symbol) in table:
                msg = f"Failed to parse token <{token.name}>"
                start = token.index
                end = start + len(token.attribute)
                raise SyntacticError.from_data("", msg, index=start, index_end=end)

            next_symbols = table[(current, symbol)]
            for next_symbol in reversed(next_symbols):
                if next_symbol != "&":
                    stack.append(next_symbol)

            if stack[-1] == symbol:
                stack.pop()
                ready_for_next = True

    return True
