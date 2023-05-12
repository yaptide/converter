import itertools
from pathlib import Path

import converter.solid_figures as solid_figures
from converter.common import Parser
from converter.shieldhit.beam import (BeamConfig, BeamSourceType,
                                      MultipleScatteringMode, StragglingModel)
from converter.shieldhit.detect import (DetectConfig, OutputQuantity,
                                        ScoringFilter, ScoringOutput)
from converter.shieldhit.geo import (DefaultMaterial, GeoMatConfig, Material,
                                     Zone)
from converter.shieldhit.scoring_geometries import (ScoringCylinder,
                                                    ScoringGeometry,
                                                    ScoringGlobal, ScoringMesh,
                                                    ScoringZone)


class ShieldhitParser(Parser):
    """A SHIELD-HIT12A parser"""

    def __init__(self) -> None:
        super().__init__()
        self.info['simulator'] = 'shieldhit'
        self.beam_config = BeamConfig()
        self.detect_config = DetectConfig()
        self.geo_mat_config = GeoMatConfig()

    def parse_configs(self, json: dict) -> None:
        """Wrapper for all parse functions"""
        self._parse_beam(json)
        self._parse_geo_mat(json)
        self._parse_detect(json)

    def _parse_beam(self, json: dict) -> None:
        """Parses data from the input json into the beam_config property"""
        self.beam_config.energy = json["beam"]["energy"]
        self.beam_config.energy_spread = json["beam"]["energySpread"]
        # we use get here to avoid KeyError if the cutoffs are not defined
        # in that case None will be inserted into the beam config
        # which is well handled by the converter
        self.beam_config.energy_low_cutoff = json["beam"].get("energyLowCutoff")
        self.beam_config.energy_high_cutoff = json["beam"].get("energyHighCutoff")
        self.beam_config.nstat = json["beam"].get("numberOfParticles", self.beam_config.nstat)
        self.beam_config.beampos = tuple(json["beam"]["position"])
        self.beam_config.beamdir = tuple(json["beam"]["direction"])

        if "sigma" in json["beam"]:
            beam_type = json["beam"]["sigma"]["type"]

            if beam_type == "Gaussian":
                self.beam_config.beam_ext_x = abs(json["beam"]["sigma"]["x"])
                self.beam_config.beam_ext_y = abs(json["beam"]["sigma"]["y"])
            elif beam_type == "Flat square":
                self.beam_config.beam_ext_x = -abs(json["beam"]["sigma"]["x"])
                self.beam_config.beam_ext_y = -abs(json["beam"]["sigma"]["y"])
            elif beam_type == "Flat circular":
                self.beam_config.beam_ext_x = 1.0  # To generate a circular beam x value must be greater than 0
                self.beam_config.beam_ext_y = -abs(json["beam"]["sigma"]["y"])

        if "sad" in json["beam"]:
            beam_type = json["beam"]["sad"]["type"]

            if beam_type == "double":
                self.beam_config.sad_x = json["beam"]["sad"]["x"]
                self.beam_config.sad_y = json["beam"]["sad"]["y"]
            elif beam_type == "single":
                self.beam_config.sad_x = json["beam"]["sad"]["x"]
                self.beam_config.sad_y = None
            else:
                self.beam_config.sad_x = None
                self.beam_config.sad_y = None

        if json["beam"].get("beamSourceType", "") == BeamSourceType.FILE.value:
            self.beam_config.beam_source_type = BeamSourceType.FILE
            self.beam_config.beam_source_file = json["beam"].get("beamSourceFile", '')

        if "physic" in json:
            self.beam_config.delta_e = json["physic"].get("energyLoss", self.beam_config.delta_e)
            self.beam_config.nuclear_reactions = json["physic"].get(
                "enableNuclearReactions", self.beam_config.nuclear_reactions)
            self.beam_config.straggling = StragglingModel.from_str(
                json["physic"].get("energyModelStraggling", self.beam_config.straggling.value))
            self.beam_config.multiple_scattering = MultipleScatteringMode.from_str(
                json["physic"].get("multipleScattering", self.beam_config.multiple_scattering.value))

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

    def _get_zone_index_by_uuid(self, zone_uuid: str) -> int:
        """Finds zone in the geo_mat_config object by its uuid and returns its simmulation index."""
        for idx, zone in enumerate(self.geo_mat_config.zones):
            if zone.uuid == zone_uuid:
                return idx + 1

        raise ValueError(f"No zone with uuid \"{zone_uuid}\".")

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

    def _get_scoring_geometry_bu_uuid(self, geo_uuid: str) -> str:
        """Finds scoring geometry in the detect_config object by its uuid and returns its simmulation name."""
        for scoring_geometry in self.detect_config.scoring_geometries:
            if scoring_geometry.uuid == geo_uuid:
                return scoring_geometry.name

        raise ValueError(f"No scoring geometry with uuid {geo_uuid}")

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

    def _get_scoring_filter_by_uuid(self, filter_uuid: str) -> str:
        """Finds scoring filter in the detect_config object by its uuid and returns its simmulation name."""
        for scoring_filter in self.detect_config.scoring_filters:
            if scoring_filter.uuid == filter_uuid:
                return scoring_filter.name

        raise ValueError(f"No scoring filter with uuid {filter_uuid} in {self.detect_config.scoring_filters}.")

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
        self.geo_mat_config.materials = [Material(material["uuid"], material["icru"])
                                         for material in json["materialManager"]["materials"]]

    def _parse_figures(self, json: dict) -> None:
        """Parse figures from JSON"""
        self.geo_mat_config.figures = [
            solid_figures.parse_figure(figure_dict) for figure_dict in json["scene"]["object"].get('children')
        ]

    def _add_overridden_material(self, material: Material) -> None:
        """Parse materials from JSON"""
        self.geo_mat_config.materials.append(material)

    def _get_material_by_uuid(self, material_uuid: str) -> Material:
        """Finds first material in the geo_mat_config object with corresponding uuid and returns it."""
        for material in self.geo_mat_config.materials:
            if material.uuid == material_uuid:
                return material

        raise ValueError(f"No material with uuid {material_uuid}.")

    def _get_material_id(self, material_uuid: str) -> int:
        """Find material by uuid and retun its id."""
        offset = 0
        for idx, material in enumerate(self.geo_mat_config.materials):

            # If the material is a DefaultMaterial then we need the value not its index,
            # the _value2member_map_ returns a map of values and members that allows us to check if
            # a given value is defined within the DefaultMaterial enum.
            if DefaultMaterial.is_default_material(material.icru):

                if material.uuid == material_uuid:
                    return int(material.icru)

                # We need to count all DefaultMaterials prior to the searched one.
                offset += 1

            elif material.uuid == material_uuid:
                # Only materials defined in mat.dat file are indexed.
                return idx + 1 - offset

        raise ValueError(f"No material with uuid {material_uuid} in materials {self.geo_mat_config.materials}.")

    def _parse_zones(self, json: dict) -> None:
        """Parse zones from JSON"""
        self.geo_mat_config.zones = [
        ]

        for idx, zone in enumerate(json["zoneManager"]["zones"]):
            if 'customMaterial' in zone and zone['customMaterial'] is not None:
                overridden_material = Material(
                    uuid=zone['customMaterial']['uuid'],
                    icru=zone['customMaterial']['icru'],
                    density=zone['customMaterial']['density'])

                self._add_overridden_material(overridden_material)

            self.geo_mat_config.zones.append(
                Zone(
                    uuid=zone["uuid"],
                    # lists are numbered from 0, but shieldhit zones are numbered from 1
                    id=idx + 1,
                    figures_operators=self._parse_csg_operations(zone["unionOperations"]),
                    material=self._get_material_id(zone["materialUuid"]),
                    material_override=zone.get('materialPropertiesOverrides', None),
                )
            )

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

    def _get_figure_index_by_uuid(self, figure_uuid: str) -> int:
        """Find the list index of a figure from geo_mat_config.figures by uuid. Usefull when parsing CSG operations."""
        for idx, figure in enumerate(self.geo_mat_config.figures):
            if figure.uuid == figure_uuid:
                return idx

        raise ValueError(f"No figure with uuid \"{figure_uuid}\".")

    def get_configs_json(self) -> dict:
        """Get JSON data for configs"""
        configs_json = {
            "info.json": str(self.info),
            "beam.dat": str(self.beam_config),
            "mat.dat": self.geo_mat_config.get_mat_string(),
            "detect.dat": str(self.detect_config),
            "geo.dat": self.geo_mat_config.get_geo_string()
        }


        if self.beam_config.beam_source_type == BeamSourceType.FILE:
            configs_json["sobp.dat"] = self.beam_config.beam_source_file['value']

        return configs_json
