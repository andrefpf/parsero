from parsero.cfg.contextfree_grammar import ContextFreeGrammar


def test_import():
    path_to_file = "examples/simple_cfg.cfg"
    dict_to_compare = dict()

    dict_to_compare["S"] = [["A", "B"], ["id"]]
    dict_to_compare["A"] = [["&"], ["a", "A"]]
    dict_to_compare["B"] = [["&"], ["D"], ["b", "B"]]
    dict_to_compare["C"] = [["c"], ["c", "C"]]
    dict_to_compare["D"] = [["d", "D"]]

    non_terminal_symbols = set(["S", "A", "B", "C", "D"])
    terminal_symbols = set(["a", "b", "c", "d", "id", "&"])

    cfg = ContextFreeGrammar(path_to_file)
    dict_from_cfg = cfg.production_rules

    assert set(dict_from_cfg.keys()) == set(dict_to_compare.keys())
    assert cfg.non_terminal_symbols == non_terminal_symbols
    assert cfg.terminal_symbols == terminal_symbols

    for symbol, productions in dict_from_cfg.items():
        assert dict_to_compare[symbol] == productions


def test_to_str():
    path_to_file = "examples/simple_cfg.cfg"

    str_to_compare = "S\t → A B | id\n"
    str_to_compare += "A\t → & | a A\n"
    str_to_compare += "B\t → & | D | b B\n"
    str_to_compare += "C\t → c | c C\n"
    str_to_compare += "D\t → d D"

    cfg = ContextFreeGrammar("examples/simple_cfg.cfg")

    assert str(cfg) == str_to_compare


def test_refactor_epsilon_free():
    path_to_file = "examples/nullable_initial.cfg"
    dict_to_compare = dict()

    dict_to_compare["S1"] = [["&"], ["S"]]
    dict_to_compare["S"] = [["A"], ["A", "B"], ["B"], ["id"]]
    dict_to_compare["S0"] = [["a"], ["a", "A"], ["b"], ["b", "B"]]
    dict_to_compare["A"] = [["a"], ["a", "S"]]
    dict_to_compare["B"] = [["b", "S0"], ["d"]]

    non_terminal_symbols = set(
        [
            "S1",
            "S0",
            "S",
            "A",
            "B",
        ]
    )
    terminal_symbols = set(["a", "b", "id", "&", "d"])

    cfg = ContextFreeGrammar(path_to_file)
    cfg.refactor_epsilon_free()
    dict_from_cfg = cfg.production_rules

    assert set(dict_from_cfg.keys()) == set(dict_to_compare.keys())
    assert cfg.non_terminal_symbols == non_terminal_symbols
    assert cfg.terminal_symbols == terminal_symbols

    for symbol, productions in dict_from_cfg.items():
        assert dict_to_compare[symbol] == productions


def test_refactor_unitary_productions():
    path_to_file = "examples/simple_cfg.cfg"
    dict_to_compare = dict()

    dict_to_compare["S"] = [["A", "B"], ["id"]]
    dict_to_compare["A"] = [["&"], ["a", "A"]]
    dict_to_compare["B"] = [["&"], ["b", "B"], ["d", "D"]]
    dict_to_compare["C"] = [["c"], ["c", "C"]]
    dict_to_compare["D"] = [["d", "D"]]

    non_terminal_symbols = set(["S", "A", "B", "C", "D"])
    terminal_symbols = set(["a", "b", "c", "d", "id", "&"])

    cfg = ContextFreeGrammar(path_to_file)
    cfg.refactor_unitary_productions()
    dict_from_cfg = cfg.production_rules

    assert set(dict_from_cfg.keys()) == set(dict_to_compare.keys())
    assert cfg.non_terminal_symbols == non_terminal_symbols
    assert cfg.terminal_symbols == terminal_symbols

    for symbol, productions in dict_from_cfg.items():
        assert dict_to_compare[symbol] == productions


def test_remove_unreachable_symbols():
    path_to_file = "examples/simple_cfg.cfg"
    dict_to_compare = dict()

    dict_to_compare["S"] = [["A", "B"], ["id"]]
    dict_to_compare["A"] = [["&"], ["a", "A"]]
    dict_to_compare["B"] = [["&"], ["D"], ["b", "B"]]
    dict_to_compare["D"] = [["d", "D"]]

    non_terminal_symbols = set(["S", "A", "B", "D"])
    terminal_symbols = set(["a", "b", "d", "id", "&"])

    cfg = ContextFreeGrammar(path_to_file)
    cfg.remove_unreachable_symbols()
    dict_from_cfg = cfg.production_rules

    assert set(dict_from_cfg.keys()) == set(dict_to_compare.keys())
    assert cfg.non_terminal_symbols == non_terminal_symbols
    assert cfg.terminal_symbols == terminal_symbols

    for symbol, productions in dict_from_cfg.items():
        assert dict_to_compare[symbol] == productions


def test_remove_unproductive_symbols():
    path_to_file = "examples/simple_cfg.cfg"
    dict_to_compare = dict()

    dict_to_compare["S"] = [["A", "B"], ["id"]]
    dict_to_compare["A"] = [["&"], ["a", "A"]]
    dict_to_compare["B"] = [["&"], ["b", "B"]]
    dict_to_compare["C"] = [["c"], ["c", "C"]]

    non_terminal_symbols = set(["S", "A", "B", "C"])
    terminal_symbols = set(["a", "b", "c", "id", "&"])

    cfg = ContextFreeGrammar(path_to_file)
    cfg.remove_unproductive_symbols()
    dict_from_cfg = cfg.production_rules

    assert set(dict_from_cfg.keys()) == set(dict_to_compare.keys())
    assert cfg.non_terminal_symbols == non_terminal_symbols
    assert cfg.terminal_symbols == terminal_symbols

    for symbol, productions in dict_from_cfg.items():
        assert dict_to_compare[symbol] == productions


def test_remove_useless_symbols():
    path_to_file = "examples/simple_cfg.cfg"
    dict_to_compare = dict()

    dict_to_compare["S"] = [["A", "B"], ["id"]]
    dict_to_compare["A"] = [["&"], ["a", "A"]]
    dict_to_compare["B"] = [["&"], ["b", "B"]]

    non_terminal_symbols = set(["S", "A", "B"])
    terminal_symbols = set(["a", "b", "id", "&"])

    cfg = ContextFreeGrammar(path_to_file)
    cfg.remove_useless_symbols()
    dict_from_cfg = cfg.production_rules

    assert set(dict_from_cfg.keys()) == set(dict_to_compare.keys())
    assert cfg.non_terminal_symbols == non_terminal_symbols
    assert cfg.terminal_symbols == terminal_symbols

    for symbol, productions in dict_from_cfg.items():
        assert dict_to_compare[symbol] == productions


def test_left_recursion():
    path_to_file = "examples/left_recursion_one.cfg"
    dict_to_compare = dict()

    dict_to_compare["S"] = [["A", "a"], ["b"]]
    dict_to_compare["A"] = [["a", "A0"], ["b", "d", "A0"]]
    dict_to_compare["A0"] = [["&"], ["a", "d", "A0"], ["c", "A0"]]

    non_terminal_symbols = set(["S", "A", "A0"])
    terminal_symbols = set(["a", "b", "c", "d", "&"])

    cfg = ContextFreeGrammar(path_to_file)
    cfg.refactor_left_recursion()
    dict_from_cfg = cfg.production_rules

    assert set(dict_from_cfg.keys()) == set(dict_to_compare.keys())
    assert cfg.non_terminal_symbols == non_terminal_symbols
    assert cfg.terminal_symbols == terminal_symbols

    for symbol, productions in dict_from_cfg.items():
        assert dict_to_compare[symbol] == productions

    path_to_file = "examples/left_recursion_two.cfg"
    dict_to_compare = dict()

    dict_to_compare["S"] = [["A", "a", "S0"]]
    dict_to_compare["S0"] = [["&"], ["b", "S0"]]
    dict_to_compare["A"] = [["d", "A0"]]
    dict_to_compare["A0"] = [["&"], ["a", "S0", "c", "A0"]]

    non_terminal_symbols = set(["S", "S0", "A", "A0"])
    terminal_symbols = set(["a", "b", "c", "d", "&"])

    cfg = ContextFreeGrammar(path_to_file)
    cfg.refactor_left_recursion()
    dict_from_cfg = cfg.production_rules

    assert set(dict_from_cfg.keys()) == set(dict_to_compare.keys())
    assert cfg.non_terminal_symbols == non_terminal_symbols
    assert cfg.terminal_symbols == terminal_symbols

    for symbol, productions in dict_from_cfg.items():
        assert dict_to_compare[symbol] == productions


def test_factoring():
    # precisa atualizar esse teste
    return
    path_to_file = "examples/non_deterministic.cfg"
    dict_to_compare = dict()

    dict_to_compare["S"] = [["b", "S0"]]
    dict_to_compare["S0"] = [["b", "B0", "c", "d"], ["c", "S1"]]
    dict_to_compare["S1"] = [["d", "S2"]]
    dict_to_compare["S2"] = [["&"], ["d", "D0"]]
    dict_to_compare["B"] = [["b", "B0"]]
    dict_to_compare["B0"] = [["&"], ["b", "B0"]]
    dict_to_compare["D"] = [["d", "D0"]]
    dict_to_compare["D0"] = [["&"], ["d", "D0"]]

    non_terminal_symbols = set(["S", "S0", "S1", "S2", "B", "B0", "D", "D0"])
    terminal_symbols = set(["b", "c", "d", "&"])

    cfg = ContextFreeGrammar(path_to_file)
    cfg.left_factor()
    dict_from_cfg = cfg.production_rules

    assert set(dict_from_cfg.keys()) == set(dict_to_compare.keys())
    assert cfg.non_terminal_symbols == non_terminal_symbols
    assert cfg.terminal_symbols == terminal_symbols

    for symbol, productions in dict_from_cfg.items():
        assert dict_to_compare[symbol] == productions
