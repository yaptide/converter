import json
from math import isclose
from dataclasses import dataclass, field
from converter.fluka.cards.compound_card import CompoundCard
from converter.fluka.cards.material_card import MaterialCard


class MaterialsConfig():
    def __init__(self):
        # icru -> material
        self.predefined_materials = {}
        # icru -> compound
        self.predefined_compounds = {}
        self.materials = []
        self.compounds = []
        self.__load_predefined_materials()
        # nmat is used to attach index to materials
        self.__nmat = max(self.predefined_materials.values(), key=lambda x: x.fluka_number).fluka_number 
    
    def parse_materials(self, materials: list) -> None:
        for material in materials:
            if material.icru not in self.predefined_materials_icru or material.icru not in self.predefined_compounds_icru:
                raise NotImplementedError("Handling of non-predefined FLUKA materials and compounds is not implemented yet.")
            if material.icru in self.predefined_materials_icru:
                if material.icru in [0, 1000]:
                    # black hole and vacuum are special cases they cannot be redefined
                    continue
                else:
                    if not isclose(material.density, self.predefined_materials[material.icru].density, rel_tol=1e-6):
                        # density is different, we need to redefine the material
                        self.__nmat += 1
                        new_material = CustomMaterial(
                            fluka_name=material.fluka_name,
                            fluka_number=self.__nmat,
                            common_name=material.common_name,
                            A=material.A,
                            Z=material.Z,
                            density=material.density
                        )
                        self.materials.append(new_material)
            if material.icru in self.predefined_compounds_icru:
                if not isclose(material.density, self.predefined_compounds[material.icru].density, rel_tol=1e-6):
                    # density is different, we need to redefine the compound
                    ratio = material.density / self.predefined_compounds[material.icru].density
                    new_compound = CustomCompound(
                        fluka_name=material.fluka_name,
                        fluka_number=self.__nmat,
                        common_name=material.common_name,
                        density=material.density
                    )
                    self.compounds.append(new_compound)


    def __load_predefined_materials(self) -> None:
        with open("materials.json", "r") as file:
            data = json.load(file)
            for material in data["materials"]:
                new_material = Material(
                    fluka_name=material["fluka_name"],
                    fluka_number=material["fluka_number"],
                    common_name=material["common_name"],
                    A=material["A"],
                    Z=material["Z"],
                    density=material["density"]
                )
                self.predefined_materials[material["icru"]] = new_material
            for compound in data["compounds"]:
                new_compound = Compound(
                    fluka_name=compound["fluka_name"],
                    fluka_number=compound["fluka_number"],
                    common_name=compound["common_name"],
                    density=compound["density"]
                )
                self.predefined_compounds[compound["icru"]] = new_compound
            

@dataclass
class Material:
    fluka_name: str
    fluka_number: int
    common_name: str
    A: float
    Z: int
    density: float # [g/cm^3] 

@dataclass
class Compound:
    fluka_name: str
    fluka_number: int
    common_name: str
    density: float # [g/cm^3]

@dataclass
class CustomMaterial(MaterialCard, Material):
    def convert_params_to_whats(self):
        self.what = [str(self.Z), "", str(self.density), str(self.fluka_number), "0", str(self.A)]
        

@dataclass
class CustomCompound(CompoundCard):
    def convert_params_to_whats(self):
        self.what = [str(self.density), str(self.fluka_number), "0", "0", "0", "0"]

