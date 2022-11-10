from parsero.contextfree_grammar import ContextFreeGrammar
from parsero.finite_automata import FiniteAutomata
from parsero.nd_finite_automata import NDFiniteAutomata
from parsero.state import State


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

    with open(path_to_file, "w") as file:
        file.write(str(number_states) + "\n")
        file.write(str(initial_state) + "\n")
        file.write(final_states + "\n")
        file.write(alphabet + "\n")

        while transitions:
            file.write(transitions.pop(0))

            if transitions:
                file.write("\n")


def file_to_contextfree_grammar(path_to_file):
    all_symbols = set()
    non_terminal_symbols = set()
    initial_symbol = ""
    productions = list()

    with open(path_to_file, "r") as file:
        while line := file.readline():
            production_pieces = line.split("->", 1)
            symbol = production_pieces[0].strip()
            non_terminal_symbols.add(symbol)

            if initial_symbol == "":
                initial_symbol = symbol

            productions_body = [prod.strip() for prod in production_pieces[1].split("|")]

            production_rule = list()

            for prod in productions_body:
                i = 0
                body = []
                while True:
                    if i == len(prod):
                        break

                    if prod[i] == "<":
                        long_symbol = prod[i]

                        while True:
                            i += 1
                            if prod[i] == ">":
                                long_symbol += ">"
                                break

                            long_symbol += prod[i]

                        body.append(long_symbol)
                        i += 1
                        continue

                    body.append(prod[i])
                    i += 1

                for s in body:
                    all_symbols.add(s)
                production_rule.append(body)

            productions.append((symbol, production_rule))

    terminal_symbols = all_symbols - non_terminal_symbols

    return ContextFreeGrammar(non_terminal_symbols, terminal_symbols, productions, initial_symbol)


def contextfree_grammar_to_file(contextfree_grammar, path_to_file):
    if type(contextfree_grammar) != ContextFreeGrammar:
        raise TypeError("Specified ContextFree Grammar is not a ContextFree Grammar.")

    productions = list()
    production_rules = contextfree_grammar.production_rules

    for symbol, production_rule in production_rules.items():
        production_rule = " | ".join(production_rule).strip()

        production = "{} -> {}".format(symbol, production_rule)
        productions.append(production)

    with open(path_to_file, "w") as file:
        while productions:
            file.write(productions.pop(0))

            if productions:
                file.write("\n")
