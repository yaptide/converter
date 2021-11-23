from abc import ABC, abstractmethod


class Parser(ABC):
    """Abstract parser, the template for implementing other parsers."""

    @abstractmethod
    def parse_configs(self, json: dict) -> None:
        """Convert the json dict to the 4 config dataclasses."""

    @abstractmethod
    def save_configs(self, target_dir: str) -> None:
        """
        Save the configs as text files in the target_dir.
        The files are: beam.dat, mat.dat, detect.dat and geo.dat.
        """

    @abstractmethod
    def get_configs_json(self) -> dict:
        """
        Return a dict representation of the config files.
        Each file is a field ("beam", "mat", "detect" and "geo") that contains
        the respective file contents.
        """
