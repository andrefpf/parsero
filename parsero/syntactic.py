from parsero.contextfree_grammar import ContextFreeGrammar


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
                        if symbol != '&':
                            first_set.add(symbol)
                        else:
                            nullable = True
            if nullable:
                first_set.add('&')
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

                                if '&' in first_of_next:
                                    first_of_next.remove('&')
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
    print(follow_dict)
    return follow_dict
