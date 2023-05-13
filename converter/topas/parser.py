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

    def get_configs_json(self) -> dict:
        """
        Return a dict representation of the config files. Each element has
        the config files name as key and its content as value.
        """
        configs_json = super().get_configs_json()
        configs_json["topas_config.txt"] = str(self.config)

        return configs_json
