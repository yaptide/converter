from converter.common import Parser
from pathlib import Path

class DummmyParser(Parser):
    """A simple placeholder parser that ignores the json input and prints example (default) configs."""

    def __init__(self) -> None:
        self.config = """s:Ge/MyBox/Type     = "TsBox"
s:Ge/MyBox/Material = "Air"
s:Ge/MyBox/Parent   = "World"
d:Ge/MyBox/HLX      = 2.5 m
d:Ge/MyBox/HLY      = 2. m
d:Ge/MyBox/HLZ      = 1. m
d:Ge/MyBox/TransX   = 2. m
d:Ge/MyBox/TransY   = 0. m
d:Ge/MyBox/TransZ   = 0. m
d:Ge/MyBox/RotX     = 0. deg
d:Ge/MyBox/RotY     = 0. deg
d:Ge/MyBox/RotZ     = 0. deg

sv:Ph/Default/Modules = 1 "g4em-standard_opt0"
"""

    def parse_configs(self, json: dict) -> None:
        """Basicaly do nothing since we work on defaults in this parser."""

    def save_configs(self, target_dir: str) -> None:
        "Save the configs as text files in the target_dir in file topas_config.txt."
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
        configs_json = {
            "topas_config.txt": self.config
        }

        return configs_json
