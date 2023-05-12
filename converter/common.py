from pathlib import Path


class Parser:
    """Abstract parser, the template for implementing other parsers."""

    def __init__(self) -> None:
        self.info = {
            "version": "",
            "label": "",
            "simulator": "",
        }

    def parse_configs(self, json: dict) -> None:
        """Convert the json dict to the 4 config dataclasses."""
        raise NotImplementedError

    def save_configs(self, target_dir: str):
        """
        Save the configs as text files in the target_dir.
        The files are: beam.dat, mat.dat, detect.dat and geo.dat.
        """
        if not Path(target_dir).exists():
            raise ValueError("Target directory does not exist.")

        for file_name, content in self.get_configs_json().items():
            with open(Path(target_dir, file_name), 'w') as conf_f:
                conf_f.write(content)

    @staticmethod
    def get_configs_json() -> dict:
        """
        Return a dict representation of the config files. Each element has
        the config files name as key and its content as value.
        """
        return {}
