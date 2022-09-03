from dataclasses import dataclass


@dataclass
class State:
    name: str
    is_final: bool
