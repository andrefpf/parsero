from parsero import regex

INDENT_FINDER = regex.compiles("(    )*")


def treat_identation(string):
    lines = string.splitlines() + [" "]
    treated_lines = []
    last_level = 0
    last_line = ""

    for line in lines:
        if not line:
            treated_lines.append(last_line)
            last_line = line
            continue

        matched, _ = INDENT_FINDER.match(line)
        level = len(matched) // 4
        diference = level - last_level

        if diference > 0:
            treated_lines.append(last_line + "↳" * diference)
            last_line = line
        elif diference < 0:
            treated_lines.append(last_line + "↲" * abs(diference))
            last_line = line
        else:
            treated_lines.append(last_line)
            last_line = line

        last_level = level

    new_string = "\n".join(treated_lines)
    return new_string
