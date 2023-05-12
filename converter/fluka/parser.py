from pathlib import Path
from converter.common import Parser
from converter.fluka.input import Input


class FlukaParser(Parser):
    """A simple placeholder that ignores the json input and prints example (default) configs."""

    def __init__(self) -> None:
        version = "unknown"
        self.info = {
            "version": version,
            "label": "development",
            "simulator": "fluka",
        }
        self.input = Input()

    def parse_configs(self, json: dict) -> None:
        """Parse energy and number of particles from json."""
        # Since energy in json is in MeV and FLUKA uses GeV, we need to convert it.
        self.input.energy = float(json["beam"]["energy"]) * 1e-3
        self.input.number_of_particles = json["beam"]["numberOfParticles"]

    def save_configs(self, target_dir: Path) -> None:
        """
        This will save the Fluka Configuration to a file named fl_sim.imp
        in the target_dir directory.
        """
        if not Path(target_dir).exists():
            raise FileNotFoundError("Target directory doest not exist.")
        for file_name, content in self.get_configs_json().items():
            with open(Path(target_dir, file_name), "w") as conf_f:
                conf_f.write(content)

    def get_configs_json(self) -> dict:
        """
        Return a dict representation of the config files. Each element has
        the config files name as key and its content as value.
        """
        configs_json = {"info.json": str(self.info), "fl_sim.inp": str(self.input)}

        return configs_json
