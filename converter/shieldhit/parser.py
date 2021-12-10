from abc import ABC
from functools import reduce
from dataclasses import dataclass, field
from os import path
from converter.common import Parser
from converter.shieldhit.geo import GeoMatConfig, Zone, parse_figure
from converter.shieldhit.detect import DetectConfig, OutputQuantity, ScoringFilter, ScoringOutput
from converter.shieldhit.scoring_geometries import ScoringGeometry, ScoringGlobal, ScoringCylinder, ScoringMesh, ScoringZone
from converter.shieldhit.beam import BeamConfig
import converter.solid_figures as solid_figures

BLACK_HOLE_MATERIAL = 0
VACUUM_MATERIAL = 1000


class DummmyParser(Parser):
    """A simple placeholder parser that ignores the json input and prints example (default) configs."""

    def __init__(self) -> None:
        self.beam_config = BeamConfig()
        self.detect_config = DetectConfig()
        self.geo_mat_config = GeoMatConfig()

    def parse_configs(self, json: dict):
        """Basicaly do nothing since we work on defaults in this parser."""

    def save_configs(self, target_dir: str):
        """
        Save the configs as text files in the target_dir.
        The files are: beam.dat, mat.dat, detect.dat and geo.dat.
        """
        target_dir = path.abspath(target_dir)

        for file_name, content in self.get_configs_json().items():
            with open(path.join(target_dir, file_name), 'w') as conf_f:
                conf_f.write(content)

    def get_configs_json(self) -> dict:
        """
        Return a dict representation of the config files. Each element has
        the config files name as key and its content as value.
        """
        configs_json = {
            "beam.dat": str(self.beam_config),
            "mat.dat": self.geo_mat_config.get_mat_string(),
            "detect.dat": str(self.detect_config),
            "geo.dat": self.geo_mat_config.get_geo_string(),
        }

        return configs_json


class ShieldhitParser(DummmyParser):
    """A regular shieldhit parser"""

    def parse_configs(self, json: dict) -> None:
        """Wrapper for all parse functions"""
        self._parse_beam(json)
        self._parse_geo_mat(json)
        self._parse_detect(json)

    def _parse_beam(self, json: dict) -> None:
        """Parses data from the input json into the beam_config property"""
        self.beam_config.energy = json["beam"]["energy"]

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
                geometries.append(ScoringCylinder(
                    name=geometry_dict["name"],
                    r_min=geometry_dict["data"]["innerRadius"],
                    r_max=geometry_dict["data"]["radius"],
                    r_bins=geometry_dict["data"]["radialSegments"],
                    h_min=geometry_dict["position"][2]-geometry_dict["data"]["radialSegments"]/2,
                    h_max=geometry_dict["position"][2]+geometry_dict["data"]["radialSegments"]/2,
                    h_bins=geometry_dict["data"]["zSegments"],
                ))
            elif geometry_dict["type"] == "Mesh":
                geometries.append(ScoringMesh(
                    name=geometry_dict["name"],
                    x_min=geometry_dict["position"][0]-geometry_dict["data"]["width"]/2,
                    x_max=geometry_dict["position"][0]+geometry_dict["data"]["width"]/2,
                    x_bins=geometry_dict["data"]["xSegments"],
                    y_min=geometry_dict["position"][1]-geometry_dict["data"]["height"]/2,
                    y_max=geometry_dict["position"][1]+geometry_dict["data"]["height"]/2,
                    y_bins=geometry_dict["data"]["ySegments"],
                    z_min=geometry_dict["position"][2]-geometry_dict["data"]["depth"]/2,
                    z_max=geometry_dict["position"][2]+geometry_dict["data"]["depth"]/2,
                    z_bins=geometry_dict["data"]["zSegments"],
                ))
            elif geometry_dict["type"] == "Zone":
                geometries.append(ScoringZone(
                    name=geometry_dict["name"],
                    first_zone_id=self._get_zone_index_by_uuid(geometry_dict["data"]["zoneUuid"]),
                ))
            elif geometry_dict["type"] == "All":
                geometries.append(ScoringGlobal(
                    name=geometry_dict["name"],
                ))
            else:
                raise ValueError("Invalid ScoringGeometry type \"{0}\".".format(geometry_dict["type"]))

            return geometries

    def _get_zone_index_by_uuid(self, uuid: str):
        for idx, zone in self.geo_mat_config.zones:
            if zone.uuid == uuid:
                return idx+1

        raise ValueError(f"No zone with uuid \"{uuid}\".")

    def _parse_scoring_filters(self, json: dict) -> list[ScoringFilter]:
        """Parses scoring filters from the input json."""
        filters = []

        return filters

    def _parse_scoring_outputs(self, json: dict) -> list[ScoringOutput]:
        """Parses scoring outputs from the input json."""
        outputs = []

        return outputs

    def _parse_geo_mat(self, json: dict) -> None:
        """Parses data from the input json into the geo_mat_config property"""
        self._parse_materials(json)
        self._parse_figures(json)
        self._parse_zones(json)

    def _parse_materials(self, json: dict) -> None:
        """Parse materials from JSON"""
        self.geo_mat_config.materials = [(material["uuid"], material["icru"])
                                         for material in json["materialManager"]["materials"]]

    def _parse_figures(self, json: dict) -> None:
        """Parse figures from JSON"""
        self.geo_mat_config.figures = [solid_figures.parse_figure(
            figure_dict) for figure_dict in json["scene"]["object"].get('children')]

    def _get_material_id(self, uuid: str) -> int:
        """Find material by uuid and retun its id."""
        for idx, item in enumerate(self.geo_mat_config.materials):
            if item[0] == uuid:
                return idx+1

        raise ValueError(f"No material with uuid {uuid} in materials {self.geo_mat_config.materials}.")

    def _parse_zones(self, json: dict) -> None:
        """Parse zones from JSON"""
        self.geo_mat_config.zones = [
            Zone(
                uuid=zone["uuid"],
                # lists are numbered from 0, but shieldhit zones are numbered from 1
                id=idx+1,
                figures_operators=self._parse_csg_operations(zone["unionOperations"]),
                material=self._get_material_id(zone["materialUuid"]),
            ) for idx, zone in enumerate(json["zoneManager"]["zones"])
        ]

        if "worldZone" in json["zoneManager"]:
            self._parse_world_zone(json)

    def _parse_world_zone(self, json: dict) -> None:
        """Parse the world zone and add it to the zone list"""
        # Add bounding figure to figures
        world_figure = solid_figures.parse_figure(json["zoneManager"]["worldZone"])
        self.geo_mat_config.figures.append(world_figure)

        self.geo_mat_config.zones.append(
            Zone(
                uuid="",
                id=len(self.geo_mat_config.zones)+1,
                # slightly larger world zone - world zone
                figures_operators=self._calculate_world_zone_operations(len(self.geo_mat_config.figures)),
                # the last material is the black hole
                material=VACUUM_MATERIAL
            )
        )

        # Add the figure that will serve as a black hole wrapper around the world zone
        # Take the world zone figure
        world_figure = solid_figures.parse_figure(json["zoneManager"]["worldZone"])
        # Make the figure slightly bigger. It will form the black hole wrapper around the simulation.
        world_figure.expand(1.)
        self.geo_mat_config.figures.append(
            world_figure
        )

        # Add the black hole wrapper
        last_figure_idx = len(self.geo_mat_config.figures)
        self.geo_mat_config.zones.append(
            Zone(
                uuid="",
                id=len(self.geo_mat_config.zones)+1,
                # slightly larger world zone - world zone
                figures_operators=[{last_figure_idx, -(last_figure_idx-1)}],
                # the last material is the black hole
                material=BLACK_HOLE_MATERIAL
            )
        )

    def _parse_csg_operations(self, operations: list[list[dict]]) -> list[set[int]]:
        """
        Parse dict of csg operations to a list of sets. Sets contain a list of intersecting geometries.
        The list contains a union of geometries from sets.
        """
        operations = [item for ops in operations for item in ops]
        parsed_operations = []
        for operation in operations:
            # lists are numbered from 0, but shieldhit figures are numbered from 1
            figure_id = self._get_figure_index_by_uuid(operation["objectUuid"])+1
            if operation["mode"] == "union":
                parsed_operations.append({figure_id})
            elif operation["mode"] == "subtraction":
                parsed_operations[-1].add(-figure_id)
            elif operation["mode"] == "intersection":
                parsed_operations[-1].add(figure_id)
            else:
                raise ValueError("Unexpected CSG operation: {1}".format(operation["mode"]))

        return parsed_operations

    def _calculate_world_zone_operations(self, world_zone_figure: int) -> list[set[int]]:
        """Calculate the world zone operations. Take the wolrd zone figure and subract all geometries."""
        # Sum all zones
        all_zones = [figure_operators for zone in self.geo_mat_config.zones
                     for figure_operators in zone.figures_operators]

        world_zone = [{world_zone_figure}]

        for figure_set in all_zones:
            new_world_zone = []
            for w_figure_set in world_zone:
                for figure in figure_set:
                    new_world_zone.append({*w_figure_set, -figure})
            world_zone = new_world_zone

        return world_zone

    def _get_figure_index_by_uuid(self, uuid: str) -> int:
        """Find the list index of a figure from geo_mat_config.figures by uuid. Usefull when parsing CSG operations."""
        figure = [figure for figure in self.geo_mat_config.figures if figure.uuid == uuid][0]
        return self.geo_mat_config.figures.index(figure)
