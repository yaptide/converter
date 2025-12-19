from typing import Optional, Set
# skipcq: BAN-B405
import xml.etree.ElementTree as ET
from defusedxml.minidom import parseString

from converter.geant4 import utils
from .materials import collect, emit
from .structure import emit_structure


def generate_gdml_entry_point(world_json: Optional[dict]) -> str:
    """Public entry: generate GDML string for provided world or an empty world."""
    if world_json:
        return _generate_gdml(world_json)
    return _generate_empty()


def _generate_gdml(world: dict) -> str:
    """Generate GDML from geometry node"""
    gdml_root = ET.Element("gdml", {
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:noNamespaceSchemaLocation":
            "http://cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd",
    })

    ET.SubElement(gdml_root, "define")

    used_materials: Set[str] = set()
    collect(world, used_materials)

    materials_xml = ET.SubElement(gdml_root, "materials")
    emit(materials_xml, used_materials)

    solids_xml = ET.SubElement(gdml_root, "solids")
    structure_xml = ET.SubElement(gdml_root, "structure")

    counters = {"solid": {}, "logic": {}, "phys": {}}

    emit_structure(
        node=world,
        solids_xml=solids_xml,
        structure_xml=structure_xml,
        counters=counters,
    )

    setup = ET.SubElement(gdml_root, "setup", {
        "name": "Default",
        "version": "1.0",
    })
    ET.SubElement(setup, "world", {
        "ref": utils.choose_logic_name(world),
    })

    return _prettify_xml(gdml_root)


def _generate_empty() -> str:
    """Generate empty GDML from geometry node"""
    root = ET.Element("gdml", {
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:noNamespaceSchemaLocation":
            "http://cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd",
    })

    ET.SubElement(root, "define")
    ET.SubElement(root, "materials")

    solids = ET.SubElement(root, "solids")
    ET.SubElement(solids, "box", {
        "name": "solidWorld",
        "x": utils.to_mm_str(100),
        "y": utils.to_mm_str(100),
        "z": utils.to_mm_str(100),
        "lunit": "mm",
    })

    structure = ET.SubElement(root, "structure")
    vol = ET.SubElement(structure, "volume", {"name": "logicWorld"})
    ET.SubElement(vol, "materialref", {"ref": "G4_Galactic"})
    ET.SubElement(vol, "solidref", {"ref": "solidWorld"})

    setup = ET.SubElement(root, "setup", {"name": "Default", "version": "1.0"})
    ET.SubElement(setup, "world", {"ref": "logicWorld"})

    return _prettify_xml(root)


def _prettify_xml(root: ET.Element) -> str:
    """Return a pretty-printed XML string for a given ElementTree root."""
    xml_bytes = ET.tostring(root, "utf-8")
    pretty = parseString(xml_bytes).toprettyxml(indent="  ")
    no_decl = "\n".join(pretty.split("\n")[1:])
    return '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + no_decl
