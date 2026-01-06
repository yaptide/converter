# skipcq: BAN-B405
import xml.etree.ElementTree as ET
from converter.geant4 import utils
from .solids import create_solid_element


def build_structure(
    node: dict,
    counters: dict,
) -> tuple[list[ET.Element], list[ET.Element], str, str]:
    """Build GDML solids and structure elements for a node and its children."""
    solids: list[ET.Element] = []
    volumes: list[ET.Element] = []

    child_infos = []

    for ch in node.get("children", []):
        ch_solids, ch_volumes, ch_logic, _ = build_structure(ch, counters)
        solids.extend(ch_solids)
        volumes.extend(ch_volumes)

        pos = ch.get("geometryData", {}).get("position", [0, 0, 0])
        child_infos.append((ch, ch_logic, pos))

    solid_name = utils.choose_solid_name(node, counters)
    solid_element = create_solid_element(node, solid_name)
    if solid_element is not None:
        solids.append(solid_element)

    logic_name = utils.choose_logic_name(node, counters)
    vol = ET.Element("volume", {"name": logic_name})

    material = node.get("simulationMaterial", {}).get(
        "geant4_name", "G4_Galactic"
    )
    ET.SubElement(vol, "materialref", {"ref": material})
    ET.SubElement(vol, "solidref", {"ref": solid_name})

    for child, child_logic, (x, y, z) in child_infos:
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

    volumes.append(vol)

    return solids, volumes, logic_name, solid_name
