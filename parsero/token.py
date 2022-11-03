from dataclasses import dataclass


@dataclass
class Token:
    name: str
    attribute: str = ""

    def __repr__(self):
        return f'<{self.name}, "{self.attribute}">'

class TokenList(list):
    pass
