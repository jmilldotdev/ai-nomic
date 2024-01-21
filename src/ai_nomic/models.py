from dataclasses import dataclass


@dataclass
class HumanPlayer:
    name: str
    score: int


@dataclass
class AgenticPlayer:
    name: str
    identity: str
    score: int
