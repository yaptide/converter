from dataclasses import dataclass

@dataclass
class ScoringCard:
    def __str__(self) -> str:
        """Return the card as a string."""
        result = ""
