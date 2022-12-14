from pathlib import Path

from parsero.automata import FiniteAutomata, NDFiniteAutomata
from parsero.automata.state import State


def file_to_automata(path_to_file):
    """
    Reads file from the specified path_to_file and returns
    the corresponding D/ND Finite Automata.
    """

    is_deterministic = True
    states = []
    initial_state = 0
    alphabet = []
    transitions = []

    with open(path_to_file, "r") as file:
        number_states = int(file.readline())
        initial_state = int(file.readline())
        final_states = [int(x) for x in file.readline().split(",")]

        for i in range(number_states):
            is_final = False
            if i in final_states:
                is_final = True

            states.append(State(str(i), is_final))

        alphabet = file.readline().strip().split(",")

        if "&" in alphabet:
            is_deterministic = False

        while line := file.readline():
            transition_parts = line.split(",")
            transition_parts[0] = int(transition_parts[0])
            transition_parts[2] = transition_parts[2].strip()

            if "-" in transition_parts[2]:
                is_deterministic = False
                transition_parts[2] = transition_parts[2].split("-")
                transition_parts[2] = tuple([int(x) for x in transition_parts[2]])
            else:
                transition_parts[2] = int(transition_parts[2])

            transitions.append(tuple(transition_parts))

    if is_deterministic:
        return FiniteAutomata(states, transitions, alphabet, initial_state)
    else:
        return NDFiniteAutomata(states, transitions, alphabet, initial_state)


def automata_to_file(automata, path_to_file):
    """
    Writes the corresponding D/ND Finite Automata to
    a file at the specified path_to_file.
    """

    if type(automata) not in [FiniteAutomata, NDFiniteAutomata]:
        raise TypeError("Specified automata is not an automata.")

    number_states = len(automata.states)
    initial_state = automata.initial_state
    transition_map = automata.transition_map

    final_states = []

    for state in automata.states:
        if state.is_final:
            final_states.append(state.name)

    final_states = ",".join(final_states)

    alphabet = ",".join(automata.alphabet)
    transitions = []

    for transition, target in transition_map.items():
        origin = str(transition[0])
        symbol = transition[1]

        if type(target) == set:
            target = "-".join(str(x) for x in target)
        else:
            target = str(target)

        transition_str = ",".join([origin, symbol, target])

        transitions.append(transition_str)

    # Creates the folder if it does not exist
    path = Path(path_to_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path_to_file, "w") as file:
        file.write(str(number_states) + "\n")
        file.write(str(initial_state) + "\n")
        file.write(final_states + "\n")
        file.write(alphabet + "\n")

        while transitions:
            file.write(transitions.pop(0))

            if transitions:
                file.write("\n")
