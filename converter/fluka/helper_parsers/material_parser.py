from dataclasses import dataclass, field
from converter.fluka.predefined_materials import (
    PREDEFINED_MATERIALS,
    PREDEFINED_COMPOUNDS,
)
from converter.fluka.helper_parsers.region_parser import FlukaRegion

BLACK_HOLE_ICRU = 0
VACUUM_ICRU = 1000
# Single elements that are sent from the UI
# have compatible icru with the atomic number
# only up to a certain number, which is
# SINGLE_ELEMENT_MAX_ICRU
SINGLE_ELEMENT_MAX_ICRU = 98


@dataclass
class FlukaMaterial:
    """Class representing a material in Fluka input"""

    fluka_name: str = ""
    fluka_number: int = 0  # Not used
    common_name: str = ""  # Not used
    A: float = 0  # Not used
    Z: int = 0
    density: float = 0
    icru: int = 0


@dataclass
class FlukaCompound:
    """Class representing a compound in Fluka input."""

    fluka_name: str = ""
    common_name: str = ""  # Not used
    density: float = 0
    # composition is a list of tuples (weight fraction, fluka name)
    composition: list[tuple[float, str]] = field(default_factory=list)


@dataclass
class MaterialAssignment:
    """Class representing an assignment of a material to a region in Fluka input."""

    material_name: str = ""
    region_name: str = ""


@dataclass
class IonisationPotential:
    """Class representing an ionisation potential in Fluka input."""

    material_name: str = ""
    ionisation_potential: float = -1.0


def load_predefined_materials() -> (list[FlukaMaterial], list[FlukaCompound]):
    """Convert list of dicts of predefined materials and compounds to lists of FlukaMaterial and FlukaCompound objects."""
    predefined_materials = {
        material.icru: FlukaMaterial(**material) for material in PREDEFINED_MATERIALS
    }
    predefined_compounds = {
        compound.icru: FlukaCompound(**compound) for compound in PREDEFINED_COMPOUNDS
    }
    return predefined_materials, predefined_compounds


def parse_materials(
    materials_json, zones_json: dict
) -> (dict[str, FlukaMaterial], dict[str, FlukaCompound]):
    predefined_materials, predefined_compounds = load_predefined_materials()
    material_index = compound_index = 1
    # uuid -> material, uuid -> compound
    materials, compounds = {}, {}
    zones = zones_json["zones"]
    if "worldZone" in zones_json:
        zones.append(zones_json["worldZone"])

    materials_list = []
    for material in materials_json:
        materials_list.append((material["uuid"], material["icru"], material["density"]))
    for zone in zones:
        if (
            "customMaterial" in zone
            and "density" in zone["materialPropertiesOverrides"]
        ):
            materials_list.append(
                (
                    zone["customMaterial"]["uuid"],
                    zone["customMaterial"]["icru"],
                    zone["materialPropertiesOverrides"]["density"],
                )
            )

    for uuid, icru, density in materials_list:
        # Check if material is black hole or vacuum, we can't redefine them,
        # however they are defined in predefined materials
        if icru in [BLACK_HOLE_ICRU, VACUUM_ICRU]:
            materials[uuid] = predefined_materials[icru]
        # Check if material is already predefined, if density is different
        # define new material
        elif icru in predefined_materials:
            predefined_material = predefined_materials[icru]
            if density != predefined_material.icru:
                new_material = FlukaMaterial(
                    fluka_name=f"MAT{material_index:0>5}",
                    Z=icru,
                    density=density,
                    icru=icru,
                )
                material_index += 1
                materials[uuid] = new_material
            else:
                materials[uuid] = predefined_material
        # Check if material is not predefined single-element
        elif icru <= SINGLE_ELEMENT_MAX_ICRU:
            new_material = FlukaMaterial(
                fluka_name=f"MAT{material_index:0>5}",
                Z=icru,
                density=density,
                icru=icru,
            )
            material_index += 1
            materials[uuid] = new_material
        # Check if material is predefined compound, if density is different
        # define new compound
        elif icru in predefined_compounds:
            predefined_compound = predefined_compounds[icru]
            if density != predefined_compound.icru:
                # To define new compound it is necessary to define new material
                new_material = FlukaMaterial(
                    fluka_name=f"COM{compound_index:0>5}",
                    Z=0,
                    density=density,
                    icru=icru,
                )
                new_compound = FlukaCompound(
                    fluka_name=f"COM{compound_index:0>5}",
                    density=density,
                    composition=[(-1.0, predefined_compound.fluka_name)],
                )
                compound_index += 1
                materials[uuid] = new_material
                compounds[uuid] = new_compound
        # If icru is not used anywhere above, it means we are dealing
        # with not predefined compound which is not supported for now
        else:
            raise NotImplementedError(f"Material with icru {icru} is not supported.")

    return materials, compounds


def assign_materials_to_regions(
    materials: dict[str, FlukaMaterial],
    regions: dict[str, FlukaRegion],
    zones_json: dict,
) -> list[MaterialAssignment]:
    """Assign materials to regions based on uuids in json."""
    assignments = []
    for zone in zones_json["zones"]:
        assignments.append(
            MaterialAssignment(
                material=materials[zone["materialUuid"]].fluka_name,
                region=regions[zone["uuid"]].name,
            )
        )
    if "worldZone" in zones_json:
        assignments.append(
            MaterialAssignment(
                material=materials[zones_json["worldZone"]["materialUuid"]].fluka_name,
                region=regions[zones_json["worldZone"]["uuid"]].name,
            )
        )
        assignments.append(
            MaterialAssignment(
                material="BLCKHOLE",
                region=regions[zones_json["worldZone"]["uuid"] + "boundary"].name,
            )
        )

    return assignments


def set_custom_ionisation_potential(
    materials: dict[str, FlukaMaterial], custom_materials: list
) -> list[IonisationPotential]:
    """Set custom ionisation potential for materials that have it defined."""
    ionisation_potentials = []
    for material in custom_materials:
        if "ionisationPotential" in material:
            ionisation_potentials.append(
                IonisationPotential(
                    material_name=materials[material["uuid"]].fluka_name,
                    ionisation_potential=material["ionisationPotential"],
                )
            )
    return ionisation_potentials
