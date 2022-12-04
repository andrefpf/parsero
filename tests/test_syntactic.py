from parsero.cfg.contextfree_grammar import ContextFreeGrammar
from parsero.lexical import Token
from parsero.syntactic import (
    calculate_first,
    calculate_follow,
    create_table,
    ll1_parse,
)


def test_first_follow_example_1():
    path_to_file = "examples/first_follow_example_1.cfg"
    cfg = ContextFreeGrammar(path_to_file)

    expected_first_dict = {
        "S": {"d", "a", "b", "c"},
        "A": {"a", "&"},
        "B": {"a", "b", "d", "&"},
        "a": {"a"},
        "b": {"b"},
        "c": {"c"},
        "d": {"d"},
        "&": {"&"},
    }

    expected_follow_dict = {
        "S": {"$"},
        "A": {"a", "b", "d", "c"},
        "B": {"c"},
    }

    first_dict = calculate_first(cfg)
    follow_dict = calculate_follow(cfg)

    assert len(first_dict) == len(expected_first_dict)
    assert len(follow_dict) == len(expected_follow_dict)

    for key, val in expected_first_dict.items():
        assert first_dict[key] == val

    for key, val in expected_follow_dict.items():
        assert follow_dict[key] == val


def test_first_follow_example_2():
    path_to_file = "examples/first_follow_example_2.cfg"
    cfg = ContextFreeGrammar(path_to_file)

    expected_first_dict = {
        "S": {"d", "a", "b", "c"},
        "A": {"a", "&"},
        "B": {"d", "a", "b", "c"},
        "C": {"c", "&"},
        "a": {"a"},
        "b": {"b"},
        "c": {"c"},
        "d": {"d"},
        "&": {"&"},
    }

    expected_follow_dict = {
        "S": {"$"},
        "A": {"b", "a", "c", "d"},
        "B": {"c", "$"},
        "C": {"d", "$"},
    }

    first_dict = calculate_first(cfg)
    follow_dict = calculate_follow(cfg)

    assert len(first_dict) == len(expected_first_dict)
    assert len(follow_dict) == len(expected_follow_dict)

    for key, val in expected_first_dict.items():
        assert first_dict[key] == val

    for key, val in expected_follow_dict.items():
        assert follow_dict[key] == val


def test_table_creation():
    path_to_file = "examples/ff_table_example.cfg"
    cfg = ContextFreeGrammar(path_to_file)
    table: dict = create_table(cfg)
    t_not = ["F", "T0"]
    t_line_end = ["&"]
    assert table[("T", "¬")] == t_not  # Just some special cases, no need to test the whole thing
    assert table[("T0", "$")] == t_line_end


def test_ll1():
    path_to_file = "examples/ff_table_example.cfg"
    cfg = ContextFreeGrammar(path_to_file)
    table: dict = create_table(cfg)
    word = ["id", "∨", "id", "∧", "id", "$"]
    tokens = [Token(i, i) for i in word]
    ll1_parse(tokens, table, cfg)
