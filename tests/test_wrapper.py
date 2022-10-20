from parsero.wrapper import *


def test_finite_automata_read():
    transitions = [
        (0, "a", 1),
        (0, "b", 1),
        (1, "a", 0),
        (1, "b", 0),
    ]

    automata = file_to_automata("tests/examples/even_chars.fa")

    assert len(automata.states) == 2
    assert automata.initial_state == 0
    assert automata.alphabet == ["a", "b"]

    transitions_automata = [
        (origin, symbol, target) for (origin, symbol), target in automata.transition_map.items()
    ]

    assert len(transitions) == len(transitions_automata)

    for transition, transition_automata in zip(transitions, transitions_automata):
        assert transition == transition_automata


def test_nd_automata_read():
    transitions = [
        (0, "a", {0}),
        (0, "b", {0, 1}),
        (1, "b", {2}),
        (2, "b", {2}),
    ]

    automata = file_to_automata("tests/examples/ends_with_bb.ndfa")

    assert len(automata.states) == 3
    assert automata.initial_state == 0
    assert automata.alphabet == ["a", "b"]

    transitions_automata = [
        (origin, symbol, target) for (origin, symbol), target in automata.transition_map.items()
    ]

    assert len(transitions) == len(transitions_automata)

    for transition, transition_automata in zip(transitions, transitions_automata):
        assert transition == transition_automata


def test_nd_automata_epsilon_read():
    transitions = [
        (0, "a", {0}),
        (1, "b", {1}),
        (2, "c", {2}),
        (0, "&", {1}),
        (1, "&", {2}),
    ]

    automata = file_to_automata("tests/examples/abc.ndfa")

    assert len(automata.states) == 3
    assert automata.initial_state == 0
    assert automata.alphabet == ["a", "b", "c", "&"]

    transitions_automata = [
        (origin, symbol, target) for (origin, symbol), target in automata.transition_map.items()
    ]

    assert len(transitions) == len(transitions_automata)

    for transition, transition_automata in zip(transitions, transitions_automata):
        assert transition == transition_automata


def test_finite_automata_write():
    automata = file_to_automata("tests/examples/even_chars.fa")

    automata_to_file(automata, "tests/output/even_chars.fa")

    with open("tests/examples/even_chars.fa") as input, open(
        "tests/output/even_chars.fa"
    ) as output:
        assert input.readline() == output.readline()


def test_nd_automata_write():
    automata = file_to_automata("tests/examples/ends_with_bb.ndfa")

    automata_to_file(automata, "tests/output/ends_with_bb.ndfa")

    with open("tests/examples/ends_with_bb.ndfa", "r") as input, open(
        "tests/output/ends_with_bb.ndfa", "r"
    ) as output:
        assert input.readline() == output.readline()


def test_nd_automata_epsilon_write():
    automata = file_to_automata("tests/examples/abc.ndfa")

    automata_to_file(automata, "tests/output/abc.ndfa")

    with open("tests/examples/abc.ndfa", "r") as input, open(
        "tests/output/abc.ndfa", "r"
    ) as output:
        assert input.readline() == output.readline()
