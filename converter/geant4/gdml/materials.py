# skipcq: BAN-B405
import xml.etree.ElementTree as ET


def collect(node: dict, acc: set[str]) -> None:
    """Collect material names appearing in geometry nodes."""
    mat = node.get("simulationMaterial", {}).get("geant4_name")

    if mat:
        acc.add(mat)

    for ch in node.get("children", []):
        collect(ch, acc)


def emit(materials_xml: ET.Element, used: set[str]) -> None:
    """if BlackHole is in materials add it to GDML file"""
    if "BlackHole" in used:
        mat = ET.SubElement(materials_xml, "material", {
            "name": "BlackHole",
            "state": "solid",
        })
        ET.SubElement(mat, "T", {"unit": "K", "value": "293.15"})
        ET.SubElement(mat, "MEE", {"unit": "eV", "value": "823"})
        ET.SubElement(mat, "D", {"unit": "g/cm3", "value": "1e+8"})
        ET.SubElement(mat, "fraction", {"n": "1", "ref": "G4_Pb"})
