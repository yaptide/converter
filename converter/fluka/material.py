import json
from math import isclose
from dataclasses import dataclass
from converter.fluka.cards.compound_card import CompoundCard
from converter.fluka.cards.material_card import MaterialCard
import random
import string
from pathlib import Path


class MaterialConfig:
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

    def parse_materials(self, materials: list) -> None:
        """Parse materials and compounds from given list of materials."""
        for material in materials:
            if material.icru in self.predefined_materials:
                if not isclose(
                    material.density, self.predefined_materials[material.icru].density
                ) and material.icru not in (0, 1000):
                    predefined_material = self.predefined_materials[material.icru]
                    new_material = CustomMaterial(
                        fluka_name=predefined_material.fluka_name,
                        fluka_number=predefined_material.fluka_number,
                        common_name=predefined_material.common_name,
                        A=predefined_material.A,
                        Z=predefined_material.Z,
                        density=material.density,
                        sdum=self.__generate_name(),
                    )
                    self.materials[material.uuid] = new_material
                else:
                    self.materials[material.uuid] = self.predefined_materials[
                        material.icru
                    ]
            elif material.icru in self.predefined_compounds:
                if not isclose(
                    material.density, self.predefined_compounds[material.icru].density
                ):
                    predefined_compound = self.predefined_compounds[material.icru]
                    new_compound = CustomCompound(
                        fluka_name=predefined_compound.fluka_name,
                        common_name=predefined_compound.common_name,
                        density=material.density,
                        sdum=self.__generate_name(),
                    )
                    new_compound.add_component(
                        -material.density / predefined_compound.density,
                        predefined_compound,
                    )
                    self.compounds[material.uuid] = new_compound
                else:
                    self.compounds[material.uuid] = self.predefined_compounds[
                        material.icru
                    ]
            else:
                raise NotImplementedError(
                    "Only predefined materials and compounds are supported."
                )

    def __load_predifined_materials(self) -> None:
        """Load predefined materials and compounds from file"""
        with open(Path(".") / "predefined_materials.json", "r") as file:
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
                self.predefined_materials[material["icru_code"]] = new_material
            for compound in data["compounds"]:
                new_compound = Compound(
                    fluka_name=compound["fluka_name"],
                    common_name=compound["common_name"],
                    density=compound["density"],
                )
                self.predefined_compounds[compound["icru_code"]] = new_compound

    def __generate_name(self) -> str:
        """Generate random name for custom material or compound."""
        while True:
            new_name = "".join(random.choices(string.ascii_uppercase, k=10))
            if new_name not in self.__names:
                self.__names.add(new_name)
                return new_name

    def get_materials(self) -> list:
        """Return list of modified materials."""
        return [
            material
            for material in self.materials.values()
            if isinstance(material, CustomMaterial)
        ]

    def get_compounds(self) -> list:
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


@dataclass
class Compound:
    """Class representing compound in FLUKA input."""

    fluka_name: str
    common_name: str
    density: float


@dataclass
class CustomMaterial(MaterialCard, Material):
    """Class representing modified material in FLUKA input."""

    def __post_init__(self):
        """Post init function, always called by automatically generated __init__."""
        self.__assign_params_to_what()

    def __assign_params_to_what(self) -> None:
        """Convert material parameters to 'what' list."""
        self.what = [self.Z, "", self.density, "", "", round(self.A)]


@dataclass
class CustomCompound(CompoundCard, Compound):
    """Class representing modified compound in FLUKA input."""
