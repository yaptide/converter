import json
from dataclasses import dataclass

class MaterialConfig():
    def __init__(self):
        self.materials = []
        self.predefined_materials = {}
        self.predefined_compounds = {}
        self.mapping_to_fluka = {}
    
    def parse_materials(self, materials: list) -> None:
        for material in materials:
            mapping = self.mapping_to_fluka[int(material["icru"])]
            if mapping in self.predefined_materials:
                self.materials[material["uuid"]] = self.predefined_materials[mapping]
            elif mapping in self.predefined_compounds:
                self.materials[material["uuid"]] = self.predefined_compounds[mapping]
        
    def _load_predefined_materials_and_mappings(self) -> None:
        """Load predefined materials and mappings from file"""
        with open("converter/fluka/materials.json", "r") as f:
            data = json.load(f)
            self.mapping_to_fluka = {int(icru) : int(fluka_mapping) for icru, fluka_mapping in data["mappings"].items()}
            self.predefined_materials = {int(id) : Material(material["fluka_name"], material["fluka_number"], material["common_name"], material["A"], material["Z"], material["denisty"]) for id, material in data["materials"].items()}
            self.predefined_compounds = {int(id) : Compound(compound["fluka_number"], compound["common_name"], compound["density"]) for id, compound in data["compounds"].items()}
        
@dataclass
class Material:
    """A class that represents a material in FLUKA."""
    fluka_name: str
    fluka_number: int
    common_name: str
    A: float # atomic mass
    Z: int # atomic number
    density: float

@dataclass
class Compound:
    """A class that represents a compound in FLUKA."""
    fluka_number: int
    common_name: str
    density: float