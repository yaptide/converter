# skipcq: BAN-B405
import xml.etree.ElementTree as ET


def collect(node: dict) -> set[str]:
    """
    Recursively traverse a geometry node tree and return a set of all
    Geant4 material names ("geant4_name") used in the subtree rooted at `node`.
    """
    materials: set[str] = set()

    mat = node.get("simulationMaterial", {}).get("geant4_name")
    if mat:
        materials.add(mat)

    for ch in node.get("children", []):
        materials.update(collect(ch))

    return materials


def create_material_elements(used: set[str]) -> list[ET.Element]:
    """Emit material definitions to GDML, including BlackHole if present in the used materials set"""
    elements: list[ET.Element] = []

    if "BlackHole" in used:
        mat = ET.Element("material", {
            "name": "BlackHole",
            "state": "solid",
        })
        ET.SubElement(mat, "T", {"unit": "K", "value": "293.15"})
        ET.SubElement(mat, "MEE", {"unit": "eV", "value": "823"})
        ET.SubElement(mat, "D", {"unit": "g/cm3", "value": "1e+8"})
        ET.SubElement(mat, "fraction", {"n": "1", "ref": "G4_Pb"})
        elements.append(mat)

    return elements
