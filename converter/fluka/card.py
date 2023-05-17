from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Card:
    """Class for a fluka card."""

    tag: str = ""
    what: Optional[List[str]] = None
    sdum: str = ""

    def __post_init__(self):
        """Post init function."""
        self.what = self.what or [""]
        self.what += [""] * (6 - len(self.what))

    def __str__(self) -> str:
        """Return the card as a string."""
        line = f"{self.tag:<10}"
        for w in self.what:
            try:
                num = float(w)
                line += f"{num:>10.3E}" if len(str(w)) > 10 else f"{num:>10}"
            except ValueError:
                line += f"{w:>10}"
        line += f"{self.sdum:<10}"
        return line
