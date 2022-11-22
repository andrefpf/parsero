from parsero.wrapper import *


def test_import():
    path_to_file = "tests/examples/simple_cfg.cfg"
    dict_to_compare = dict()

    dict_to_compare["S"] = [["A", "B"], ["id"]]
    dict_to_compare["A"] = [["&"], ["a", "A"]]
    dict_to_compare["B"] = [["&"], ["D"], ["b", "B"]]
    dict_to_compare["C"] = [["c"], ["c", "C"]]
    dict_to_compare["D"] = [["&"], ["d", "D"]]

    non_terminal_symbols = set(["S", "A", "B", "C", "D"])
    terminal_symbols = set(["a", "b", "c", "d", "id", "&"])

    cfg = file_to_contextfree_grammar(path_to_file)
    dict_from_cfg = cfg.production_rules

    assert set(dict_from_cfg.keys()) == set(dict_to_compare.keys())
    assert cfg.non_terminal_symbols == non_terminal_symbols
    assert cfg.terminal_symbols == terminal_symbols

    for symbol, productions in dict_from_cfg.items():
        assert dict_to_compare[symbol] == productions


def test_to_str():
    path_to_file = "tests/examples/simple_cfg.cfg"

    str_to_compare = "S\t → A B | id\n"
    str_to_compare += "A\t → & | a A\n"
    str_to_compare += "B\t → & | D | b B\n"
    str_to_compare += "C\t → c | c C\n"
    str_to_compare += "D\t → & | d D"

    cfg = file_to_contextfree_grammar("tests/examples/simple_cfg.cfg")

    assert str(cfg) == str_to_compare


def test_epsilon_free():
    path_to_file = "tests/examples/simple_cfg.cfg"
    dict_to_compare = dict()

    dict_to_compare["S"] = [["&"], ["A"], ["A", "B"], ["B"], ["id"]]
    dict_to_compare["A"] = [["a"], ["a", "A"]]
    dict_to_compare["B"] = [["D"], ["b"], ["b", "B"]]
    dict_to_compare["C"] = [["c"], ["c", "C"]]
    dict_to_compare["D"] = [["d"], ["d", "D"]]

    non_terminal_symbols = set(["S", "A", "B", "C", "D"])
    terminal_symbols = set(["a", "b", "c", "d", "id", "&"])

    cfg = file_to_contextfree_grammar(path_to_file)
    cfg.simplify_epsilon_free()
    dict_from_cfg = cfg.production_rules

    assert set(dict_from_cfg.keys()) == set(dict_to_compare.keys())
    assert cfg.non_terminal_symbols == non_terminal_symbols
    assert cfg.terminal_symbols == terminal_symbols

    for symbol, productions in dict_from_cfg.items():
        assert dict_to_compare[symbol] == productions

def test_unitary_productions():
    path_to_file = "tests/examples/simple_cfg.cfg"
    dict_to_compare = dict()

    dict_to_compare["S"] = [["A", "B"], ["id"]]
    dict_to_compare["A"] = [["&"], ["a", "A"]]
    dict_to_compare["B"] = [["&"], ["b", "B"], ["d", "D"]]
    dict_to_compare["C"] = [["c"], ["c", "C"]]
    dict_to_compare["D"] = [["&"], ["d", "D"]]

    non_terminal_symbols = set(["S", "A", "B", "C", "D"])
    terminal_symbols = set(["a", "b", "c", "d", "id", "&"])

    cfg = file_to_contextfree_grammar(path_to_file)
    cfg.simplify_unitary_productions()
    dict_from_cfg = cfg.production_rules

    assert set(dict_from_cfg.keys()) == set(dict_to_compare.keys())
    assert cfg.non_terminal_symbols == non_terminal_symbols
    assert cfg.terminal_symbols == terminal_symbols

    for symbol, productions in dict_from_cfg.items():
        assert dict_to_compare[symbol] == productions

def test_factoring():
    # TODO corrigir path
    path_to_file = "tests/examples/non_deterministic.cfg"
    cfg = file_to_contextfree_grammar(path_to_file)
    cfg.left_factor()

    # path_to_model = "examples/left_factored.cfg"
    # model_cfg = file_to_contextfree_grammar(path_to_model)
    # TODO achar um bom jeito de comparar os dicionarios
