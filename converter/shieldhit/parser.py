import itertools
from pathlib import Path
from converter.shieldhit.geo import DefaultMaterial
from converter.common import Parser
from converter.shieldhit.geo import GeoMatConfig, Zone
from converter.shieldhit.detect import DetectConfig, OutputQuantity, ScoringFilter, ScoringOutput
from converter.shieldhit.scoring_geometries import (ScoringGeometry, ScoringGlobal, ScoringCylinder, ScoringMesh,
                                                    ScoringZone)
from converter.shieldhit.beam import BeamConfig
import converter.solid_figures as solid_figures


class DummmyParser(Parser):
    """A simple placeholder parser that ignores the json input and prints example (default) configs."""

    def __init__(self) -> None:
        self.beam_config = BeamConfig()
        self.detect_config = DetectConfig()
        self.geo_mat_config = GeoMatConfig()
        self.info = {
                    "version": "not implemented",
                    "label": "placeholder",
                    "simulator": "shieldhit",
                }

    def parse_configs(self, json: dict):
        """Basicaly do nothing since we work on defaults in this parser."""

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

    def get_configs_json(self) -> dict:
        """
        Return a dict representation of the config files. Each element has
        the config files name as key and its content as value.
        """
        configs_json = {
            "info.json": str(self.info),
            "beam.dat": str(self.beam_config),
            "mat.dat": self.geo_mat_config.get_mat_string(),
            "detect.dat": str(self.detect_config),
            "geo.dat": self.geo_mat_config.get_geo_string(),
        }

        return configs_json


class ShieldhitParser(DummmyParser):
    """A regular SHIELD-HIT12A parser"""

    def __init__(self) -> None:
        super().__init__()
        # Add version variable to deploy script
        version = "unknown"
        self.info = {
            "version": version,
            "label": "development",
            "simulator": "shieldhit",
        }

    def parse_configs(self, json: dict) -> None:
        """Wrapper for all parse functions"""
        self._parse_beam(json)
        self._parse_geo_mat(json)
        self._parse_detect(json)

    def _parse_beam(self, json: dict) -> None:
        """Parses data from the input json into the beam_config property"""
        self.beam_config.energy = json["beam"]["energy"]
        self.beam_config.energy_spread = json["beam"]["energySpread"]
        self.beam_config.nstat = json["beam"].get("numberOfParticles", self.beam_config.nstat)
        self.beam_config.beampos = tuple(json["beam"]["position"])
        self.beam_config.beamdir = tuple(json["beam"]["direction"])

    def _parse_detect(self, json: dict) -> None:
        """Parses data from the input json into the detect_config property"""
        self.detect_config.scoring_geometries = self._parse_scoring_geometries(json)
        self.detect_config.scoring_filters = self._parse_scoring_filters(json)
        self.detect_config.scoring_outputs = self._parse_scoring_outputs(json)

    def _parse_scoring_geometries(self, json: dict) -> list[ScoringGeometry]:
        """Parses scoring geometries from the input json."""
        geometries = []
        for geometry_dict in json["detectManager"]["detectGeometries"]:
            if geometry_dict["type"] == "Cyl":
                geometries.append(
                    ScoringCylinder(
                        uuid=geometry_dict["uuid"],
                        name=geometry_dict["name"],
                        r_min=geometry_dict["data"]["innerRadius"],
                        r_max=geometry_dict["data"]["radius"],
                        r_bins=geometry_dict["data"]["radialSegments"],
                        h_min=geometry_dict["position"][2] - geometry_dict["data"]["depth"] / 2,
                        h_max=geometry_dict["position"][2] + geometry_dict["data"]["depth"] / 2,
                        h_bins=geometry_dict["data"]["zSegments"],
                    ))
            elif geometry_dict["type"] == "Mesh":
                geometries.append(
                    ScoringMesh(
                        uuid=geometry_dict["uuid"],
                        name=geometry_dict["name"],
                        x_min=geometry_dict["position"][0] - geometry_dict["data"]["width"] / 2,
                        x_max=geometry_dict["position"][0] + geometry_dict["data"]["width"] / 2,
                        x_bins=geometry_dict["data"]["xSegments"],
                        y_min=geometry_dict["position"][1] - geometry_dict["data"]["height"] / 2,
                        y_max=geometry_dict["position"][1] + geometry_dict["data"]["height"] / 2,
                        y_bins=geometry_dict["data"]["ySegments"],
                        z_min=geometry_dict["position"][2] - geometry_dict["data"]["depth"] / 2,
                        z_max=geometry_dict["position"][2] + geometry_dict["data"]["depth"] / 2,
                        z_bins=geometry_dict["data"]["zSegments"],
                    ))
            elif geometry_dict["type"] == "Zone":
                geometries.append(
                    ScoringZone(
                        uuid=geometry_dict["uuid"],
                        name=geometry_dict["name"],
                        first_zone_id=self._get_zone_index_by_uuid(geometry_dict["data"]["zoneUuid"]),
                    ))
            elif geometry_dict["type"] == "All":
                geometries.append(ScoringGlobal(
                    uuid=geometry_dict["uuid"],
                    name=geometry_dict["name"],
                ))
            else:
                raise ValueError(f"Invalid ScoringGeometry type: {geometry_dict['type']}")

        return geometries

    def _get_zone_index_by_uuid(self, uuid: str) -> int:
        """Finds zone in the geo_mat_config object by its uuid and returns its simmulation index."""
        for idx, zone in enumerate(self.geo_mat_config.zones):
            if zone.uuid == uuid:
                return idx + 1

        raise ValueError(f"No zone with uuid \"{uuid}\".")

    @staticmethod
    def _parse_scoring_filters(json: dict) -> list[ScoringFilter]:
        """Parses scoring filters from the input json."""
        filters = [
            ScoringFilter(
                uuid=filter_dict["uuid"],
                name=filter_dict["name"],
                rules=[(rule_dict["keyword"], rule_dict["operator"], rule_dict["value"])
                       for rule_dict in filter_dict["rules"]],
            ) for filter_dict in json["detectManager"]["filters"]
        ]

        return filters

    def _parse_scoring_outputs(self, json: dict) -> list[ScoringOutput]:
        """Parses scoring outputs from the input json."""
        outputs = [
            ScoringOutput(
                filename=output_dict["name"] + ".bdo",
                fileformat=output_dict["fileFormat"] if "fileFormat" in output_dict else "",
                geometry=self._get_scoring_geometry_bu_uuid(output_dict["detectGeometry"])
                if 'detectGeometry' in output_dict else None,
                medium=output_dict["medium"] if 'medium' in output_dict else None,
                offset=output_dict["offset"] if 'offset' in output_dict else None,
                primaries=output_dict["primaries"] if 'primaries' in output_dict else None,
                quantities=[self._parse_output_quantity(quantity)
                            for quantity in output_dict["quantities"]["active"]] if 'quantities' in output_dict else [],
                rescale=output_dict["rescale"] if 'rescale' in output_dict else None,
            ) for output_dict in json["scoringManager"]["scoringOutputs"]
        ]

        return outputs

    def _get_scoring_geometry_bu_uuid(self, uuid: str) -> str:
        """Finds scoring geometry in the detect_config object by its uuid and returns its simmulation name."""
        for scoring_geometry in self.detect_config.scoring_geometries:
            if scoring_geometry.uuid == uuid:
                return scoring_geometry.name

        raise ValueError(f"No scoring geometry with uuid {uuid}")

    def _parse_output_quantity(self, quantity_dict: dict) -> OutputQuantity:
        """Parse a single output quantity."""
        diff1 = None
        diff1_t = None
        diff2 = None
        diff2_t = None

        if len(quantity_dict["modifiers"]) >= 1:
            diff1 = (
                quantity_dict["modifiers"][0]["lowerLimit"],
                quantity_dict["modifiers"][0]["upperLimit"],
                quantity_dict["modifiers"][0]["binsNumber"],
                quantity_dict["modifiers"][0]["isLog"],
            )
            diff1_t = quantity_dict["modifiers"][0]["diffType"]

        if len(quantity_dict["modifiers"]) >= 2:
            diff2 = (
                quantity_dict["modifiers"][1]["lowerLimit"],
                quantity_dict["modifiers"][1]["upperLimit"],
                quantity_dict["modifiers"][1]["binsNumber"],
                quantity_dict["modifiers"][1]["isLog"],
            )
            diff2_t = quantity_dict["modifiers"][1]["diffType"]

        return OutputQuantity(
            detector_type=quantity_dict["keyword"],
            filter_name=self._get_scoring_filter_by_uuid(quantity_dict["filter"]) if "filter" in quantity_dict else "",
            diff1=diff1,
            diff1_t=diff1_t,
            diff2=diff2,
            diff2_t=diff2_t,
        )

    def _get_scoring_filter_by_uuid(self, uuid: str) -> str:
        """Finds scoring filter in the detect_config object by its uuid and returns its simmulation name."""
        for scoring_filter in self.detect_config.scoring_filters:
            if scoring_filter.uuid == uuid:
                return scoring_filter.name

        raise ValueError(f"No scoring filter with uuid {uuid} in materials {self.detect_config.scoring_filters}.")

    def _parse_geo_mat(self, json: dict) -> None:
        """Parses data from the input json into the geo_mat_config property"""
        self._parse_title(json)
        self._parse_materials(json)
        self._parse_figures(json)
        self._parse_zones(json)

    def _parse_title(self, json: dict) -> None:
        """Parses data from the input json into the geo_mat_config property"""
        if "title" in json["project"] and len(json["project"]["title"]) > 0:
            self.geo_mat_config.title = json["project"]["title"]

    def _parse_materials(self, json: dict) -> None:
        """Parse materials from JSON"""
        self.geo_mat_config.materials = [(material["uuid"], material["icru"])
                                         for material in json["materialManager"]["materials"]]

    def _parse_figures(self, json: dict) -> None:
        """Parse figures from JSON"""
        self.geo_mat_config.figures = [
            solid_figures.parse_figure(figure_dict) for figure_dict in json["scene"]["object"].get('children')
        ]

    def _get_material_id(self, uuid: str) -> int:
        """Find material by uuid and retun its id."""
        offset = 0
        for idx, [mat_uuid, mat_value] in enumerate(self.geo_mat_config.materials):

            # If the material is a DefaultMaterial then we need the value not its index,
            # the _value2member_map_ returns a map of values and members that allows us to check if
            # a given value is defined within the DefaultMaterial enum.
            if DefaultMaterial.is_default_material(mat_value):

                if mat_uuid == uuid:
                    return int(mat_value)

                # We need to count all DefaultMaterials prior to the searched one.
                offset += 1

            elif mat_uuid == uuid:
                # Only materials defined in mat.dat file are indexed.
                return idx + 1 - offset

        raise ValueError(f"No material with uuid {uuid} in materials {self.geo_mat_config.materials}.")

    def _parse_zones(self, json: dict) -> None:
        """Parse zones from JSON"""
        self.geo_mat_config.zones = [
            Zone(
                uuid=zone["uuid"],
                # lists are numbered from 0, but shieldhit zones are numbered from 1
                id=idx + 1,
                figures_operators=self._parse_csg_operations(zone["unionOperations"]),
                material=self._get_material_id(zone["materialUuid"]),
            ) for idx, zone in enumerate(json["zoneManager"]["zones"])
        ]

        if "worldZone" in json["zoneManager"]:
            self._parse_world_zone(json)

    def _parse_world_zone(self, json: dict) -> None:
        """Parse the world zone and add it to the zone list"""
        # Add bounding figure to figures
        world_zone = json["zoneManager"]["worldZone"]
        world_figure = solid_figures.parse_figure(world_zone)
        self.geo_mat_config.figures.append(world_figure)

        operations = self._calculate_world_zone_operations(len(self.geo_mat_config.figures))
        material = self._get_material_id(world_zone["materialUuid"])
        # add zone to zones for every operation in operations
        for operation in operations:
            self.geo_mat_config.zones.append(
                Zone(
                    uuid='',
                    id=len(self.geo_mat_config.zones) + 1,
                    # world zone defined by bounding figure and contained zones
                    figures_operators=[operation],
                    # the material of the world zone is usually defined as vacuum
                    material=material))

        # Adding Black Hole wrapper outside of the World Zone is redundant
        # if the World Zone already is made of Black Hole
        if material != DefaultMaterial.BLACK_HOLE.value:

            # Add the figure that will serve as a black hole wrapper around the world zone
            black_hole_figure = solid_figures.parse_figure(world_zone)

            # Make the figure slightly bigger. It will form the black hole wrapper around the simulation.
            black_hole_figure.expand(1.)

            # Add the black hole figure to the figures list
            self.geo_mat_config.figures.append(black_hole_figure)

            # Add the black hole wrapper zone to the zones list
            last_figure_idx = len(self.geo_mat_config.figures)
            self.geo_mat_config.zones.append(
                Zone(
                    uuid="",
                    id=len(self.geo_mat_config.zones) + 1,
                    # slightly larger world zone - world zone
                    figures_operators=[{last_figure_idx, -(last_figure_idx - 1)}],
                    # the last material is the black hole
                    material=DefaultMaterial.BLACK_HOLE))

    def _parse_csg_operations(self, operations: list[list[dict]]) -> list[set[int]]:
        """
        Parse dict of csg operations to a list of sets. Sets contain a list of intersecting geometries.
        The list contains a union of geometries from sets.
        """
        operations = [item for ops in operations for item in ops]
        parsed_operations = []
        for operation in operations:
            # lists are numbered from 0, but shieldhit figures are numbered from 1
            figure_id = self._get_figure_index_by_uuid(operation["objectUuid"]) + 1
            if operation["mode"] == "union":
                parsed_operations.append({figure_id})
            elif operation["mode"] == "subtraction":
                parsed_operations[-1].add(-figure_id)
            elif operation["mode"] == "intersection":
                parsed_operations[-1].add(figure_id)
            else:
                raise ValueError(f"Unexpected CSG operation: {operation['mode']}")

        return parsed_operations

    def _calculate_world_zone_operations(self, world_zone_figure: int) -> list[set[int]]:
        """Calculate the world zone operations. Take the wolrd zone figure and subract all geometries."""
        # Sum all zones
        all_zones = [
            figure_operators for zone in self.geo_mat_config.zones for figure_operators in zone.figures_operators
        ]

        world_zone = [{world_zone_figure}]

        for figure_set in all_zones:
            new_world_zone = []
            for w_figure_set in world_zone:
                for figure in figure_set:
                    new_world_zone.append({*w_figure_set, -figure})
            world_zone = new_world_zone

        # filter out sets containing oposite pairs of values
        world_zone = filter(lambda x: not any(abs(i) == abs(j) for i, j in itertools.combinations(x, 2)), world_zone)

        return world_zone

    def _get_figure_index_by_uuid(self, uuid: str) -> int:
        """Find the list index of a figure from geo_mat_config.figures by uuid. Usefull when parsing CSG operations."""
        for idx, figure in enumerate(self.geo_mat_config.figures):
            if figure.uuid == uuid:
                return idx

        raise ValueError(f"No figure with uuid \"{uuid}\".")
