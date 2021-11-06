from converter.common import Parser


class DummmyParser(Parser):
    """A simple placeholder parser that does nothing."""

    def __init__(self) -> None:
        raise NotImplementedError("Don't use me, i don't work yet :(")

    def parse_configs(self, json: dict) -> None:
        """Basicaly do nothing since we work on defaults in this parser."""

    def save_configs(self, target_dir: str) -> None:
        """Does nothing, not implemented yet."""
