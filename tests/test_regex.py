from parsero import regex


def test_compile():
    automata = regex.compiles(r"a(a|b)*a|b(a|b)*b|a|b")

    valid = [
        "a",
        "b",
        "aa",
        "bb",
        "aabbababbbbabababa",
        "baabbababbbbababab",
    ]

    invalid = [
        "ab",
        "ba",
        "abababababab",
        "bababababa",
    ]

    for string in valid:
        assert automata.evaluate(string)

    for string in invalid:
        assert not automata.evaluate(string)


def test_match():
    code = "s0m3 w0rds_th4t 4re p0ss1ble variables"
    matched = regex.match(r"(\s|\w(\w|\d|_)*)*", code)
    assert matched == "s0m3 w0rds_th4t "


def test_evaluate():
    assert not regex.evaluate("goo+gle", "ggle")
    assert not regex.evaluate("goo+gle", "gogle")
    assert regex.evaluate("goo+gle", "google")
    assert regex.evaluate("goo+gle", "gooooooooooooooooooogle")

    assert not regex.evaluate("sus(pect)?", "suspects")
    assert not regex.evaluate("sus(pect)?", "su")
    assert regex.evaluate("sus(pect)?", "suspect")
    assert regex.evaluate("sus(pect)?", "sus")


def test_file_regex():
    automatas = regex.from_file("examples/example_1.regex")

    assert automatas["digit"].evaluate("2")
    assert automatas["digit"].evaluate("5")
    assert not automatas["digit"].evaluate("81")
    assert not automatas["digit"].evaluate("a")

    assert automatas["letter"].evaluate("a")
    assert automatas["letter"].evaluate("b")
    assert not automatas["letter"].evaluate("oi")
    assert not automatas["letter"].evaluate("5")

    assert automatas["id"].evaluate("banana")
    assert automatas["id"].evaluate("andrezinhogameplay2001")
    assert not automatas["id"].evaluate("007Teste")
    assert not automatas["id"].evaluate("200bananas")


def test_escaped():
    """
    la bestialidad
    """

    teste = "(um)(dois)(tr.es)(q.u+a*t|r,o)"

    matched = regex.match(r"\(um\)", teste)
    assert matched == "(um)"

    matched = regex.match(r"(\(\w*\))*", teste)
    assert matched == "(um)(dois)"

    matched = regex.match(r"(\(\w*(\.\w*)*\))*", teste)
    assert matched == "(um)(dois)(tr.es)"

    matched = regex.match(r"(\(\w*((\.|\+|\*|\||,)\w*)*\))*", teste)
    assert matched == "(um)(dois)(tr.es)(q.u+a*t|r,o)"
