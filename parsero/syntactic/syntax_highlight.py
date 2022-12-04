from parsero import Parser
from parsero.syntactic import treat_identation
from parsero.common.errors import LexicalError, SyntacticError
from termcolor import colored
from itertools import cycle


def define_colors(parser):
    colors = ["blue", "white", "red", "cyan", "yellow"]
    token_dict = dict()
    
    for ids in parser.lexical.keywords:
        token_dict[ids] = "magenta"

    for ids, color in zip(parser.lexical.token_ids, cycle(colors)):
        if "bracket" in ids:
            color = "blue"

        if ids == "comment":
            color = "green"

        token_dict[ids] = color    
    
    return token_dict


def highlight(parser, path):
    separator = "\n" + (100 * "_") + "\n\n"
    token_dict = define_colors(parser)
    last_error = None

    with open(path) as file:
        string = file.read()
    
    string = treat_identation(string)
    remaining = ""
    
    try:
        parser.parse(path)
    except LexicalError as error:
        last_error = error
        remaining = string[error.index:]
        string = string[:error.index]
    except SyntacticError as error:
        last_error = error
        remaining = string[error.index:]
        string = string[:error.index]

    output = []
    last_index = 0
    tokens = parser.lexical.tokenize_string(string)
    for token in tokens:
        inter_tokens = string[last_index:token.index]
        lexeme = colored(token.attribute, token_dict[token.name])
        output.append(inter_tokens)
        output.append(lexeme)
        last_index += len(inter_tokens) + len(token.attribute)

    if last_error is not None:
        error_part = colored(remaining, "white", "on_red")
        output.append(error_part)
        output.append(separator)
        output.append(colored(str(last_error), "red"))

    reconstructed = ''.join(output)
    return reconstructed


if __name__ == "__main__":
    parser = Parser("examples/python/python.regex", "examples/python/python.ghm")
    string = highlight(parser, "examples/python/example.py")
    print(string)