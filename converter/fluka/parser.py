from converter.common import Parser
from converter.fluka.helper_parsers.beam_parser import parse_beam
from converter.fluka.helper_parsers.figure_parser import parse_figures
from converter.fluka.helper_parsers.region_parser import parse_regions
from converter.fluka.helper_parsers.scoring_parser import parse_scorings
from converter.fluka.helper_parsers.material_parser import (
    parse_materials,
    assign_materials_to_regions,
    set_custom_ionisation_potential,
)
from converter.fluka.input import Input


class FlukaParser(Parser):
    """
    A simple parser that parses only some of the parameters, such as geometry data and beam energy,
    and returns hardcoded values for other parameters
    """

    def __init__(self) -> None:
        super().__init__()
        self.info["simulator"] = "fluka"
        self.info["version"] = "unknown"
        self.input = Input()

    def parse_configs(self, json: dict) -> None:
        """Parse energy and number of particles from json."""
        self.input.number_of_particles = json["beam"]["numberOfParticles"]
        self.input.figures = parse_figures(json["figureManager"].get("figures"))
        regions, world_figures = parse_regions(json["zoneManager"], self.input.figures)
        self.input.scorings = parse_scorings(json["detectorManager"], json["scoringManager"])
        self.input.regions = list(regions.values())
        self.input.figures.extend(world_figures)
        materials, compounds, self.input.lowmats = parse_materials(json["materialManager"]["materials"],
                                                                   json["zoneManager"])
        self.input.materials = [
            material for material in materials.values() if material.fluka_name.startswith(("MAT", "COM"))
        ]
        self.input.compounds = [compound for compound in compounds.values() if compound.fluka_name.startswith("COM")]
        self.input.assignmats = assign_materials_to_regions(materials, regions, json["zoneManager"])
        self.input.matprops = set_custom_ionisation_potential(materials, json["zoneManager"],
                                                              json["materialManager"]["materials"])
        self.input.beam = parse_beam(json["beam"])

    def get_configs_json(self) -> dict:
        """
        Return a dict representation of the config files. Each element has
        the config files name as key and its content as value.
        """
        configs_json = super().get_configs_json()
        configs_json["fl_sim.inp"] = str(self.input)

        return configs_json
