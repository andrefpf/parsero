from dataclasses import dataclass


@dataclass
class Token:
    name: str
    attribute: str = ''
