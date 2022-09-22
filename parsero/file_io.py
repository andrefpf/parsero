from state import State
from finite_automata import FiniteAutomata
from nd_finite_automata import NDFiniteAutomata

def file_to_automata(path_to_file):
    """
    Reads file from the specified path_to_file and returns
    the corresponding D/ND Finite Automata.
    """

    is_deterministic = True
    states = []
    initial_state = 0
    transitions = []

    file = open(path_to_file, 'r')

    number_states = int(file.readline())
    initial_state = int(file.readline())
    final_states = [int(x) for x in file.readline().split(',')]

    for i in range(number_states):
        is_final = False
        if i in final_states:
            is_final = True

        states.append(State(str(i), is_final))

    alphabet = file.readline().replace('\n', '').split(',')

    if '&' in alphabet:
        is_deterministic = False

    while line := file.readline():
        transition_parts = line.split(',')
        transition_parts[0] = int(transition_parts[0])
        transition_parts[2] = transition_parts[2].replace('\n', '')

        if '-' in transition_parts[2]:
            is_deterministic = False
            transition_parts[2] = transition_parts[2].split('-')
            transition_parts[2] = tuple([int(x) for x in transition_parts[2]])
        else:
            transition_parts[2] = int(transition_parts[2])
        
        transitions.append(tuple(transition_parts))

    if is_deterministic:
        return FiniteAutomata(states, initial_state, transitions)
    else:
        return NDFiniteAutomata(states, initial_state, transitions)
