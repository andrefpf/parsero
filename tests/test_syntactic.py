from parsero.cfg.contextfree_grammar import ContextFreeGrammar
from parsero.syntactic import *


def test_first_follow_example_1():
    path_to_file = "examples/first_follow_example_1.cfg"
    cfg = ContextFreeGrammar(path_to_file)
    expected_first = {"d", "a", "b", "c"}
    assert first("S", cfg) == expected_first

    expected_follow_S = {"$"}
    expected_follow_B = {"c"}
    expected_follow_A = {"a", "b", "d", "c"}

    follow_result = syntactic_analyzer.follow(cfg)
    assert follow_result["S"] == expected_follow_S
    assert follow_result["B"] == expected_follow_B
    assert follow_result["A"] == expected_follow_A


def test_first_follow_example_2():
    path_to_file = "examples/first_follow_example_2.cfg"
    cfg = ContextFreeGrammar(path_to_file)
    expected_first_S = {"d", "a", "b", "c"}
    expected_first_A = {"a", "&"}
    expected_first_B = {"d", "a", "b", "c"}
    expected_first_C = {"c", "&"}

    assert syntactic_analyzer.first("S", cfg) == expected_first_S
    assert syntactic_analyzer.first("A", cfg) == expected_first_A
    assert syntactic_analyzer.first("B", cfg) == expected_first_B
    assert syntactic_analyzer.first("C", cfg) == expected_first_C

    expected_follow_S = {"$"}
    expected_follow_A = {"b", "a", "c", "d"}
    expected_follow_B = {"c", "$"}
    expected_follow_C = {"d", "$"}

    follow_result = syntactic_analyzer.follow(cfg)
    assert follow_result["S"] == expected_follow_S
    assert follow_result["A"] == expected_follow_A
    assert follow_result["B"] == expected_follow_B
    assert follow_result["C"] == expected_follow_C


def test_table_creation():
    path_to_file = "examples/ff_table_example.cfg"
    cfg = ContextFreeGrammar(path_to_file)
    table: dict = syntactic_analyzer.create_table(cfg)
    t_not = ["F", "T0"]
    t_line_end = ["&"]
    assert table[("T", "¬")] == t_not  # Just some special cases, no need to test the whole thing
    assert table[("T0", "$")] == t_line_end


def test_ll1():
    path_to_file = "examples/ff_table_example.cfg"
    cfg = ContextFreeGrammar(path_to_file)
    table: dict = syntactic_analyzer.create_table(cfg)
    word = ["id", "∨", "id", "∧", "id", "$"]
    assert syntactic_analyzer.ll1_parse(word, table, cfg) == True
