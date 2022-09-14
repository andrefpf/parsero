from parsero.nd_finite_automata import NDFiniteAutomata

alphanumericals = alphanumerical.closure()


def concatenation_automata(string):
    states = [State(f"q{i}") for i in range(len(string))]
    transitions = [(i, char, i + 1) for i in enumerate(string)]
    return NDFiniteAutomata(states=states, transitions=transitions)


def compile_regex(string: str) -> NDFiniteAutomata:
    # if it is a common expression return the corresponding automata

    or_operation = False
    automata = NDFiniteAutomata()

    i = 0
    while i < len(string):
        if string[i] == "*":
            if or_operation:
                raise ValueError(f"Invalid sequence of symbols |* on {i}")

            automata = automata.closure()
            continue

        if string[i] == "|":
            or_operation = True
            continue

        # If a word appear, make a recursive call to compute the word
        word_size = alphanumericals.match(string[i:])
        if word_size:
            current_automata = concatenation_automata(string[i : i + word_size])
            i += word_size

        # If a expression between brackets appear, make a recursive call to compute the expression
        elif string[i] == "(":
            end = next_closing_brackets()
            current_automata = compile_regex(string[i:end])
            i += end

        else:
            raise ValueError(f"Unknown symbol {string[i]} at position {i}")

        if or_operation:
            or_operation = False
            automata = automata | current_automata
        else:
            automata = automata + current_automata

    return automata
