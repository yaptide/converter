import json
from dataclasses import dataclass
from converter.fluka.cards.compound_card import CompoundCard
from converter.fluka.cards.material_card import MaterialCard
import random
import string
from pathlib import Path


class MaterialsCompoundsConfig:
    """Class for managing materials and compounds."""

    def __init__(self):
        # icru -> material
        self.predefined_materials = {}
        # icru -> compound
        self.predefined_compounds = {}
        # uuid -> material
        self.materials = {}
        # uuid -> compound
        self.compounds = {}
        self.__names = set()
        self.__load_predifined_materials()

    def parse_materials_compounds(self, materials: list, zones: list) -> None:
        """Parse materials and compounds from lists of materials and zones."""
        for material in materials:
            uuid = material["uuid"]
            icru = material["icru"]
            density = material["density"]
            self.__add_new_material_compound(uuid, icru, density)
        for zone in zones:
            if "density" in zone["materialPropertiesOverrides"]:
                uuid = zone["materialUuid"]
                density = zone["materialPropertiesOverrides"]["density"]
                icru = zone["customMaterial"]["icru"]
                self.__add_new_material_compound(uuid, icru, density)

    def __add_new_material_compound(self, uuid, icru, density) -> None:
        """Add new material or compound to the list of materials or compounds."""
        if icru in self.predefined_materials:
            if density != self.predefined_materials[icru].density and icru not in (0, 1000):
                predefined_material = self.predefined_materials[icru]
                new_material = CustomMaterial(
                    fluka_name=predefined_material.fluka_name,
                    fluka_number=None,
                    common_name=predefined_material.common_name,
                    A=predefined_material.A,
                    Z=predefined_material.Z,
                    density=density,
                    sdum=self.__generate_name(),
                )
                self.materials[uuid] = new_material
            else:
                self.materials[uuid] = self.predefined_materials[icru]
        elif icru in self.predefined_compounds:
            if density != self.predefined_compounds[icru].density:
                predefined_compound = self.predefined_compounds[icru]
                new_compound = CustomCompound(
                    fluka_name=predefined_compound.fluka_name,
                    common_name=predefined_compound.common_name,
                    density=density,
                    sdum=self.__generate_name(),
                )
                new_compound.add_component(
                    -density / predefined_compound.density,
                    predefined_compound,
                )
                self.compounds[uuid] = new_compound
            else:
                self.compounds[uuid] = self.predefined_compounds[icru]
        else:
            raise NotImplementedError(
                "Only predefined materials and compounds are supported."
            )

    def __load_predifined_materials(self) -> None:
        """Load predefined materials and compounds from file"""
        with open(
            Path("__file__").resolve().parent
            / "converter"
            / "fluka"
            / "predefined_materials.json",
            "r",
        ) as file:
            data = json.load(file)
            for material in data["materials"]:
                new_material = Material(
                    fluka_name=material["fluka_name"],
                    fluka_number=material["fluka_number"],
                    common_name=material["common_name"],
                    A=material["A"],
                    Z=material["Z"],
                    density=material["density"],
                )
                self.predefined_materials[material["icru"]] = new_material
                self.__names.add(material["fluka_name"])
            for compound in data["compounds"]:
                new_compound = Compound(
                    fluka_name=compound["fluka_name"],
                    common_name=compound["common_name"],
                    density=compound["density"],
                )
                self.predefined_compounds[compound["icru"]] = new_compound
                self.__names.add(compound["fluka_name"])

    def __generate_name(self, length: int = 8) -> str:
        """Generate random name for custom material or compound."""
        while True:
            new_name = "".join(random.choices(string.ascii_uppercase, k=length))
            if new_name not in self.__names:
                self.__names.add(new_name)
                return new_name

    def get_custom_materials(self) -> list:
        """Return list of modified materials."""
        return [
            material
            for material in self.materials.values()
            if isinstance(material, CustomMaterial)
        ]

    def get_custom_compounds(self) -> list:
        """Return list of modified compounds."""
        return [
            compound
            for compound in self.compounds.values()
            if isinstance(compound, CustomCompound)
        ]


@dataclass
class Material:
    """Class representing material in FLUKA input."""

    fluka_name: str
    fluka_number: int
    common_name: str
    A: float
    Z: int
    density: float

    def get_name(self) -> str:
        """Return material name."""
        return self.fluka_name


@dataclass
class Compound:
    """Class representing compound in FLUKA input."""

    fluka_name: str
    common_name: str
    density: float

    def get_name(self) -> str:
        """Return compound name."""
        return self.fluka_name


@dataclass
class CustomMaterial(MaterialCard, Material):
    """Class representing modified material in FLUKA input."""

    def __post_init__(self):
        """Post init function, always called by automatically generated __init__."""
        self.__assign_params_to_what()

    def __assign_params_to_what(self) -> None:
        """Convert material parameters to 'what' list."""
        self.what = [self.Z, "", self.density, "", "", round(self.A)]

    def get_name(self) -> str:
        """Return material name."""
        return self.sdum


@dataclass
class CustomCompound(CompoundCard, Compound):
    """Class representing modified compound in FLUKA input."""

    def get_name(self) -> str:
        """Return compound name."""
        return self.sdum
