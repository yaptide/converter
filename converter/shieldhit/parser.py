from abc import ABC
from functools import reduce
from dataclasses import dataclass, field
from os import path
from converter.common import Parser
from converter.shieldhit.geo import GeoMatConfig, Zone, parse_figure
import converter.solid_figures as solid_figures


@dataclass(frozen=True)
class Geometry(ABC):
    """Abstract geometry dataclass for DetectConfig."""


@dataclass(order=True, frozen=True)
class Cylinder(Geometry):
    """Cylinder geometry dataclass used in DetectConfig."""

    sort_index: int = field(init=False)

    id: str
    radius: int = 1
    height: int = 400

    template: str = """Geometry Cyl
    Name ScoringCylinder
    R 0.0 10.0 {cyl_nr:d}
    Z 0.0 30.0 {cyl_nz:d}"""

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.id)

    def __str__(self) -> str:
        return self.template.format(cyl_nr=self.radius, cyl_nz=self.height)


@dataclass(order=True, frozen=True)
class Mesh(Geometry):
    """Mesh geometry dataclass used in DetectConfig."""

    sort_index: int = field(init=False)

    id: str
    x: int = 1
    y: int = 100
    z: int = 300

    template: str = """Geometry Mesh
    Name MyMesh_YZ
    X -5.0  5.0    {mesh_nx:d}
    Y -5.0  5.0    {mesh_ny:d}
    Z  0.0  30.0   {mesh_nz:d}"""

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.id)

    def __str__(self) -> str:
        return self.template.format(mesh_nx=self.x, mesh_ny=self.y, mesh_nz=self.z)


@dataclass
class BeamConfig:
    """Class mapping of the beam.dat config file."""

    energy: float = 150.
    nstat: int = 1000

    beam_template: str = """
RNDSEED      	89736501     ! Random seed
JPART0       	2            ! Incident particle type
TMAX0      	{energy:3.6f}   0.0  ! Incident energy; (MeV/nucl)
NSTAT       {nstat:d}    -1 ! NSTAT, Step of saving
STRAGG          2            ! Straggling: 0-Off 1-Gauss, 2-Vavilov
MSCAT           2            ! Mult. scatt 0-Off 1-Gauss, 2-Moliere
NUCRE           0            ! Nucl.Reac. switcher: 1-ON, 0-OFF
"""

    def __str__(self) -> str:
        return self.beam_template.format(energy=self.energy, nstat=self.nstat)


@dataclass
class DetectConfig:
    """Class mapping of the detect.dat config file."""

    geometries: list[Geometry] = field(default_factory=lambda: [Cylinder(id=0), Mesh(id=0)])

    detect_template = """Output
    Filename mesh.bdo
    Geo ScoringCylinder
    Quantity Dose
    """

    def __str__(self):
        detect_strings = [str(geo)
                          for geo in self.geometries] + [self.detect_template]
        return "\n".join(detect_strings)


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

    def _parse_geo_mat(self, json: dict) -> None:
        """Parses data from the input json into the geo_mat_config property"""
        self._parse_materials(json)
        self._parse_figures(json)
        self._parse_zones(json)

    def _parse_materials(self, json: dict) -> None:
        """Parse materials from JSON"""
        self.geo_mat_config.materials = [material["data"]["id"] for material in json["materialsManager"]]

    def _parse_figures(self, json: dict) -> None:
        """Parse figures from JSON"""
        self.geo_mat_config.figures = [solid_figures.parse_figure(
            figure_dict) for figure_dict in json["scene"]["object"].get('children')]

    def _parse_zones(self, json: dict) -> None:
        """Parse zones from JSON"""
        self.geo_mat_config.zones = [
            Zone(
                # lists are numbered from 0, but shieldhit zones are numbered from 1
                id=idx+1,
                figures_operators=self._parse_csg_operations(zone["unionOperations"]),
                # lists are numbered from 0, but shieldhit materials are numbered from 1
                material=self.geo_mat_config.materials.index(zone["materialData"]["id"])+1,
            ) for idx, zone in enumerate(json["zonesManager"]["zones"])
        ]

        # TODO: Update json examples
        # if "boundingZone" in json["zonesManager"]:
        #     self._parse_world_zone(json)

    def _parse_world_zone(self, json: dict) -> None:
        """Parse the world zone and add it to the zone list"""
        # Add bounding figure to figures
        self.geo_mat_config.figures.append(
            solid_figures.parse_figure(json["zonesManager"]["boundingZone"])
        )
        # Add the figure that will serve as a black hole wrapper around the bounding zone
        self.geo_mat_config.figures.append(
            solid_figures.parse_figure(json["zonesManager"]["boundingZone"]).expand(1.)
        )

        last_figure_idx = len(self.geo_mat_config.figures)-1
        self.geo_mat_config.zones.append(
            Zone(
                id=len(self.geo_mat_config.zones)+1,
                # slightly larger world zone - world zone
                figures_operators=self._calculate_world_zone_operations(last_figure_idx),
                # the last material is the black hole
                material=len(self.geo_mat_config.materials)-1)
        )

        # TODO: Make this a valid black hole material
        self.geo_mat_config.materials.append("BH")

        # Add the black hole wrapper
        self.geo_mat_config.zones.append(
            Zone(
                id=len(self.geo_mat_config.zones)+1,
                # slightly larger world zone - world zone
                figures_operators=[{last_figure_idx, -(last_figure_idx-1)}],
                # the last material is the black hole
                material=len(self.geo_mat_config.materials)-1)
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
            for w_figure_set in world_zone:
                new_world_zone = [w_figure_set.add(-figure) for figure in figure_set]
            world_zone = new_world_zone

        return world_zone

    def _get_figure_index_by_uuid(self, uuid: str) -> int:
        """Find the list index of a figure from geo_mat_config.figures by uuid. Usefull when parsing CSG operations."""
        figure = [figure for figure in self.geo_mat_config.figures if figure.uuid == uuid][0]
        return self.geo_mat_config.figures.index(figure)
