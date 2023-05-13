from converter.common import Parser
from converter.topas.config import Config
from pathlib import Path


class TopasParser(Parser):
    """A simple placeholder parser that parses energy and number of particles."""

    def __init__(self) -> None:
        super().__init__()
        self.info['simulator'] = 'topas'
        self.config = Config()

    def parse_configs(self, json: dict) -> None:
        """Basicaly do nothing since we work on defaults in this parser."""
        self.config.energy = json["beam"]["energy"]
        self.config.num_histories = json["beam"].get("numberOfParticles", self.config.num_histories)

    def save_configs(self, target_dir: str) -> None:
        """Save the configs as text files in the target_dir in file topas_config.txt."""
        if not Path(target_dir).exists():
            raise ValueError("Target directory does not exist.")

        for file_name, content in self.get_configs_json().items():
            with open(Path(target_dir, file_name), 'w') as conf_f:
                conf_f.write(content)

    def get_configs_json(self) -> dict:
        """
        Return a dict representation of the config files. Each element has
        the config files name as key and its content as value.
        """
        configs_json = super().get_configs_json()
        configs_json["topas_config.txt"] = str(self.config)

        return configs_json
