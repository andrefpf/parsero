from parsero.automata import *


def test_finite_automata_read():
    path_to_file = "examples/even_chars.fa"

    transitions = [
        (0, "a", 1),
        (0, "b", 1),
        (1, "a", 0),
        (1, "b", 0),
    ]

    automata = file_to_automata(path_to_file)

    assert len(automata.states) == 2
    assert automata.initial_state == 0
    assert automata.alphabet == ["a", "b"]

    transitions_automata = [
        (origin, symbol, target) for (origin, symbol), target in automata.transition_map.items()
    ]

    assert len(transitions) == len(transitions_automata)

    for transition, transition_automata in zip(transitions, transitions_automata):
        assert transition == transition_automata


def test_nd_finite_automata_read():
    path_to_file = "examples/ends_with_bb.ndfa"

    transitions = [
        (0, "a", {0}),
        (0, "c", {0}),
        (0, "b", {0, 1}),
        (1, "b", {2}),
        (2, "b", {2}),
    ]

    automata = file_to_automata(path_to_file)

    assert len(automata.states) == 3
    assert automata.initial_state == 0
    assert automata.alphabet == ["a", "b", "c"]

    transitions_automata = [
        (origin, symbol, target) for (origin, symbol), target in automata.transition_map.items()
    ]

    assert len(transitions) == len(transitions_automata)

    for transition, transition_automata in zip(transitions, transitions_automata):
        assert transition == transition_automata


def test_nd_finite_automata_epsilon_read():
    path_to_file = "examples/abc.ndfa"

    transitions = [
        (0, "a", {0}),
        (1, "b", {1}),
        (2, "c", {2}),
        (0, "&", {1}),
        (1, "&", {2}),
    ]

    automata = file_to_automata(path_to_file)

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
    path_to_file_read = "examples/even_chars.fa"
    path_to_file_write = "examples/output/even_chars.fa"

    automata = file_to_automata(path_to_file_read)
    automata_to_file(automata, path_to_file_write)

    with open(path_to_file_read, "r") as input, open(path_to_file_write, "r") as output:
        assert input.readline() == output.readline()


def test_nd_finite_automata_write():
    path_to_file_read = "examples/ends_with_bb.ndfa"
    path_to_file_write = "examples/output/ends_with_bb.ndfa"

    automata = file_to_automata(path_to_file_read)
    automata_to_file(automata, path_to_file_write)

    with open(path_to_file_read, "r") as input, open(path_to_file_write, "r") as output:
        assert input.readline() == output.readline()


def test_nd_finite_automata_epsilon_write():
    path_to_file_read = "examples/abc.ndfa"
    path_to_file_write = "examples/output/abc.ndfa"

    automata = file_to_automata(path_to_file_read)
    automata_to_file(automata, path_to_file_write)

    with open(path_to_file_read, "r") as input, open(path_to_file_write, "r") as output:
        assert input.readline() == output.readline()
