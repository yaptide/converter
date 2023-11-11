from dataclasses import dataclass, field
from common import format_float


@dataclass
class Card:
    """Class representing one line (card) in Fluka input."""

    codewd: str = ""
    what: list[str] = field(default_factory=list)
    sdum: str = ""

    def __post_init__(self):
        """Post init function, always called by automatically generated __init__."""
        if len(self.what) > 6:
            raise ValueError("'what' list can have at most 6 elements.")
        self.what += [""] * (6 - len(self.what))

    def __str__(self) -> str:
        """Return the card as a string."""
        return self._format_line(self.codewd, self.what, self.sdum)
    
    def _format_line(codewd: str, what: list, sdum: str) -> str:
        """Return formatted line from given parameters."""
        line = f"{codewd:<10}"
        for w in what:
            try:
                num = float(w)
                num = format_float(num, 10)
                line += f"{num:>10}"
            except ValueError:
                line += f"{w:>10}"
        line += f"{sdum:<10}"
        return line
