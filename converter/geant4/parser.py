from converter.common import Parser
from converter.geant4.macro.builder import generate_macro_entry_point
from converter.geant4.gdml.builder import generate_gdml_entry_point


class Geant4Parser(Parser):
    """Parser that converts JSON simulation configurations into GDML geometry and GEANT4 macro scripts."""

    def __init__(self):
        super().__init__()
        self.info["simulator"] = "geant4"
        self._gdml_content = ""
        self._macro_content = ""

    def parse_configs(self, json_data: dict) -> None:
        """Parse full JSON configuration into internal GDML and macro builders."""
        world = None
        if "figureManager" in json_data and json_data["figureManager"]["figures"]:
            world = json_data["figureManager"]["figures"][0]

        self._gdml_content = generate_gdml_entry_point(world)
        self._macro_content = generate_macro_entry_point(json_data)

    def get_configs_json(self) -> dict:
        """Return the full configuration JSON including generated GDML and macro data."""
        cfg = super().get_configs_json()
        cfg.update({
            "geometry.gdml": self._gdml_content,
            "run.mac": self._macro_content,
        })
        return cfg
