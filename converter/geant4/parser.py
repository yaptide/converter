from converter.common import Parser
from converter.geant4.macro.builder import Geant4MacroBuilder
from converter.geant4.gdml.builder import Geant4GDMLBuilder

class Geant4Parser(Parser):

    def __init__(self):
        super().__init__()
        self.info["simulator"] = "geant4"
        self._gdml_content = ""
        self._macro_content = ""

    def parse_configs(self, json_data: dict) -> None:
        world = None
        if "figureManager" in json_data and json_data["figureManager"]["figures"]:
            world = json_data["figureManager"]["figures"][0]

        self._gdml_content = Geant4GDMLBuilder(world).generate()
        self._macro_content = Geant4MacroBuilder(json_data).generate()

    def get_configs_json(self) -> dict:
        cfg = super().get_configs_json()
        cfg.update({
            "geometry.gdml": self._gdml_content,
            "run.mac": self._macro_content,
        })
        return cfg