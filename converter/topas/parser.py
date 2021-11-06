from converter.common import Parser

class DummmyParser(Parser):
    """A simple placeholder parser that does nothing."""

    def __init__(self) -> None:
        pass

    def parse_configs(self, json: dict):
        """Basicaly do nothing since we work on defaults in this parser."""
        pass

    def save_configs(self, target_dir: str):
        """
        Does nothing, not implemented yet.
        """
        pass
