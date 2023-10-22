from dataclasses import dataclass, field


@dataclass
class ZonesCard:
    """Class representing description of zones in Fluka input"""
    data: list = field(default_factory=lambda: [])

    def __str__(self) -> str:
        """Return the card as a string."""

        return ""