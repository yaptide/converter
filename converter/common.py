from abc import ABC, abstractmethod


class Parser(ABC):
    """Abstract parser, the template for implementing other parsers."""

    @abstractmethod
    def parse_configs(self, json: dict):
        """Convert the json dict to the 4 config dataclasses."""

    @abstractmethod
    def save_configs(self, target_dir: str):
        """
        Save the configs as text files in the target_dir.
        The files are: beam.dat, mat.dat, detect.dat and geo.dat.
        """
