from parsero.wrapper import *


def test_factoring():
    path_to_file = "tests/examples/non_deterministic.cfg"
    cfg = file_to_contextfree_grammar(path_to_file)
    cfg.left_factor()

    # path_to_model = "examples/left_factored.cfg"
    # model_cfg = file_to_contextfree_grammar(path_to_model)
    # TODO achar um bom jeito de comparar os dicionarios
