from converter.common import Parser
from converter.fluka.helper_parsers.figure_parser import parse_figures
from converter.fluka.helper_parsers.region_parser import parse_regions
from converter.fluka.input import Input
from converter.fluka.material import MaterialConfig
from converter.fluka.material import MaterialConfig


class FlukaParser(Parser):
    """
    A simple parser that parses only some of the parameters, such as geometry data and beam energy,
    and returns hardcoded values for other parameters
    """

    def __init__(self) -> None:
        super().__init__()
        self.info['simulator'] = 'fluka'
        self.info['version'] = 'unknown'
        self.input = Input()
        self.material_config = MaterialConfig()
        self.material_config = MaterialConfig()

    def parse_configs(self, json: dict) -> None:
        """Parse energy and number of particles from json."""
        # Since energy in json is in MeV and FLUKA uses GeV, we need to convert it.
        self.input.energy_GeV = float(json["beam"]["energy"]) * 1e-3
        self.input.number_of_particles = json["beam"]["numberOfParticles"]

        self._parse_materials(json["materialManager"].get("materials"))
        self.input.figures = parse_figures(json["figureManager"].get('figures'))
        self.input.regions, world_figures = parse_regions(json["zoneManager"], self.input.figures)
        self.input.figures.extend(world_figures)

    def get_configs_json(self) -> dict:
        """
        Return a dict representation of the config files. Each element has
        the config files name as key and its content as value.
        """
        configs_json = super().get_configs_json()
        configs_json["fl_sim.inp"] = str(self.input)

        return configs_json

    def _parse_materials(self, json: dict) -> None:
        """Parse materials from json."""
        self.material_config.parse_materials(json)
        self.input.materials = self.material_config.materials
        self.input.compounds = self.material_config.compounds