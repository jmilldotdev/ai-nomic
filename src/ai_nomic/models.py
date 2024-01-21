from dataclasses import dataclass


@dataclass
class HumanPlayer:
    name: str
    score: int = 0


@dataclass
class AgenticPlayer:
    name: str
    identity: str
    score: int = 0
