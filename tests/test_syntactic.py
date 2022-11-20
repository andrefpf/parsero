from parsero import syntactic
from parsero.wrapper import file_to_contextfree_grammar


def test_first_follow_example_1():
    path_to_file = "tests/examples/first_follow_example_1.cfg"
    cfg = file_to_contextfree_grammar(path_to_file)
    expected_first = {'d', 'a', 'b', 'c'}
    assert syntactic.first("S", cfg) == expected_first

    expected_follow_S = {'$'}
    expected_follow_B = {'c'}
    expected_follow_A = {'a', 'b', 'd', 'c'}

    follow_result = syntactic.follow(cfg)
    assert follow_result["S"] == expected_follow_S
    assert follow_result["B"] == expected_follow_B
    assert follow_result["A"] == expected_follow_A


def test_first_follow_example_2():
    path_to_file = "tests/examples/first_follow_example_2.cfg"
    cfg = file_to_contextfree_grammar(path_to_file)
    expected_first_S = {'d', 'a', 'b', 'c'}
    expected_first_A = {'a', '&'}
    expected_first_B = {'d', 'a', 'b', 'c'}
    expected_first_C = {'c', '&'}

    assert syntactic.first("S", cfg) == expected_first_S
    assert syntactic.first("A", cfg) == expected_first_A
    assert syntactic.first("B", cfg) == expected_first_B
    assert syntactic.first("C", cfg) == expected_first_C

    expected_follow_S = {'$'}
    expected_follow_A = {'b', 'a', 'c', 'd'}
    expected_follow_B = {'c', '$'}
    expected_follow_C = {'d', '$'}

    follow_result = syntactic.follow(cfg)
    assert follow_result["S"] == expected_follow_S
    assert follow_result["A"] == expected_follow_A
    assert follow_result["B"] == expected_follow_B
    assert follow_result["C"] == expected_follow_C
