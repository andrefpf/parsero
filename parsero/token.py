from dataclasses import dataclass


@dataclass
class Token:
    name: str
    attribute: str = ""
    index: int = 0

    def __hash__(self):
        pair = (self.name, self.attribute)
        return hash(pair)

    def __repr__(self):
        return f"<{self.name}, {self.attribute}>"


class TokenList(list):
    pass
