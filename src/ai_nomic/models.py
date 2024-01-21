from dataclasses import dataclass
from typing import Optional


@dataclass
class Player:
    name: str
    agent: bool = False
    identity: Optional[str] = None
    score: int = 0
