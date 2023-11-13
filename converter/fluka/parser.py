from converter.common import Parser
from converter.fluka.helper_parsers.figure_parser import parse_figures
from converter.fluka.helper_parsers.region_parser import parse_regions, FlukaRegion
from converter.fluka.input import Input
from converter.fluka.material import MaterialsCompoundsConfig
from converter.fluka.cards.assignmat_card import AssignMatCard


class FlukaParser(Parser):
    """
    A simple parser that parses only some of the parameters, such as geometry data, beam energy,
    and materials data, and returns hardcoded values for other parameters
    """

    def __init__(self) -> None:
        super().__init__()
        self.info["simulator"] = "fluka"
        self.info["version"] = "unknown"
        self.input = Input()
        self.materials_compounds_config = MaterialsCompoundsConfig()

    def parse_configs(self, json: dict) -> None:
        """Parse energy and number of particles from json."""
        # Since energy in json is in MeV and FLUKA uses GeV, we need to convert it.
        self.input.energy_GeV = float(json["beam"]["energy"]) * 1e-3
        self.input.number_of_particles = json["beam"]["numberOfParticles"]

        self.materials_compounds_config.parse_materials_compounds(
            materials=json["materialManager"]["materials"],
            zones=json["zoneManager"]["zones"] + [json["zoneManager"]["worldZone"]],
        )
        self.input.materials = self.materials_compounds_config.get_custom_materials()
        self.input.compounds = self.materials_compounds_config.get_custom_compounds()
        self.input.figures = parse_figures(json["figureManager"].get("figures"))
        regions, boundary_region, world_figures = parse_regions(json["zoneManager"], self.input.figures)
        self.input.regions = list(regions.values()) + [boundary_region]
        self.input.figures.extend(world_figures)
        self.__assign_materials_and_compounds(
            regions=regions,
            zones=json["zoneManager"]["zones"] + [json["zoneManager"]["worldZone"]],
            boundary=boundary_region,
        )

    def get_configs_json(self) -> dict:
        """
        Return a dict representation of the config files. Each element has
        the config files name as key and its content as value.
        """
        configs_json = super().get_configs_json()
        configs_json["fl_sim.inp"] = str(self.input)

        return configs_json

    def __assign_materials_and_compounds(self, regions: dict, zones: list, boundary: FlukaRegion) -> None:
        """Assign materials and compounds to regions."""
        assignmat_cards = []
        materials = self.materials_compounds_config.get_parsed_materials_and_compounds()
        for zone in zones:
            assignmat_cards.append(
                AssignMatCard(
                    region_name=regions[zone["uuid"]].name, material_name=materials[zone["materialUuid"]].get_name()
                )
            )
        assignmat_cards.append(AssignMatCard(region_name=boundary.name))
        self.input.assignmats = assignmat_cards
