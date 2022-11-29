from abc import ABC, abstractmethod
from pathlib import Path


class Parser(ABC):
    """Abstract parser, the template for implementing other parsers."""

    @abstractmethod
    def parse_configs(self, json: dict) -> None:
        """Convert the json dict to the 4 config dataclasses."""

    @abstractmethod
    def save_configs(self, target_dir: Path) -> None:
        """
        Save the configs as text files in the target_dir.
        The files are: beam.dat, mat.dat, detect.dat and geo.dat.
        """

    @abstractmethod
    def get_configs_json(self) -> dict:
        """
        Return a dict representation of the config files. Each element has
        the config files name as key and its content as value.
        """
