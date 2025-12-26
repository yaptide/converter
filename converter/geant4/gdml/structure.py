# skipcq: BAN-B405
import xml.etree.ElementTree as ET
from converter.geant4 import utils
from .solids import create_solid_element


def emit_structure(
    node: dict,
    solids_xml: ET.Element,
    structure_xml: ET.Element,
    counters: dict,
) -> tuple[str, str]:
    """Recursively emit GDML solids and structure definitions for a node and its children"""
    children = []

    for ch in node.get("children", []):
        logic_name, _ = emit_structure(
            ch, solids_xml, structure_xml, counters
        )
        pos = ch.get("geometryData", {}).get("position", [0, 0, 0])
        children.append((ch, logic_name, pos))

    solid_name = utils.choose_solid_name(node, counters)
    solid_element = create_solid_element(node, solid_name)
    if solid_element is not None:
        solids_xml.append(solid_element)

    logic_name = utils.choose_logic_name(node, counters)
    vol = ET.SubElement(structure_xml, "volume", {"name": logic_name})

    material = node.get("simulationMaterial", {}).get(
        "geant4_name", "G4_Galactic"
    )
    ET.SubElement(vol, "materialref", {"ref": material})
    ET.SubElement(vol, "solidref", {"ref": solid_name})

    for child, child_logic, (x, y, z) in children:
        phys_name = utils.choose_phys_name(child, counters)
        phys = ET.SubElement(vol, "physvol", {
            "copynumber": "1",
            "name": phys_name,
        })
        ET.SubElement(phys, "volumeref", {"ref": child_logic})

        if abs(x) > utils.EPS or abs(y) > utils.EPS or abs(z) > utils.EPS:
            ET.SubElement(phys, "position", {
                "name": f"{phys_name}_pos",
                "unit": "mm",
                "x": utils.to_mm_str(x),
                "y": utils.to_mm_str(y),
                "z": utils.to_mm_str(z),
            })

    return logic_name, solid_name
