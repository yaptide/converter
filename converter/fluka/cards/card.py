from dataclasses import dataclass, field


@dataclass(frozen=False)
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
        """Return card as string."""
        return self._format_line().rstrip()

    def _format_line(self) -> str:
        """Return formatted line from given parameters."""
        line = f"{self.codewd:<10}"
        for w in self.what:
            try:
                num = float(w)
                if len(str(w)) > 10:
                    # input string too long for 10-character field - use scientific notation
                    line += f"{num:>10.3E}"
                elif num.is_integer() and len(str(num)) > 10:
                    # 9+ digit integers (e.g. heavy ion codes) don't fit in 10 chars with ".0" - print as int
                    line += f"{int(num):>10}"
                else:
                    line += f"{num:>10}"
            except ValueError:
                line += f"{w:>10}"
        line += f"{self.sdum:<10}"
        return line
