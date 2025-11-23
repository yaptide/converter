
from typing import Optional, Set
# skipcq: BAN-B405
import xml.etree.ElementTree as ET
from defusedxml.minidom import parseString
import converter.geant4.utils as utils
from .materials import MaterialCollector, MaterialEmitter
from .structure import StructureEmitter


class Geant4GDMLBuilder:
    """Generates GDML geometry trees from JSON geometry nodes."""

    def __init__(self, world_json: Optional[dict]):
        self.world_json = world_json

    def generate(self) -> str:
        """Public entry: generate GDML string for provided world or an empty world."""
        if self.world_json:
            return self._generate_gdml(self.world_json)
        return self._generate_empty()

    def _generate_gdml(self, world: dict) -> str:
        """Generate GDML from geometry node"""
        gdml_root = ET.Element("gdml", {
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:noNamespaceSchemaLocation": "http://cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd",
        })

        ET.SubElement(gdml_root, "define")

        used_materials: Set[str] = set()
        MaterialCollector.collect(world, used_materials)

        materials_xml = ET.SubElement(gdml_root, "materials")
        MaterialEmitter.emit(materials_xml, used_materials)

        solids_xml = ET.SubElement(gdml_root, "solids")
        structure_xml = ET.SubElement(gdml_root, "structure")

        name_counters = {"solid": {}, "logic": {}, "phys": {}}

        emitter = StructureEmitter(solids_xml, structure_xml, name_counters)
        emitter.emit(world)

        setup_xml = ET.SubElement(gdml_root, "setup", {"name": "Default", "version": "1.0"})
        ET.SubElement(setup_xml, "world", {"ref": utils.choose_logic_name(world)})

        return self._prettify_xml(gdml_root)

    def _generate_empty(self) -> str:
        """Generate empty GDML from geometry node"""
        root = ET.Element("gdml", {
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:noNamespaceSchemaLocation": "http://cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd",
        })
        ET.SubElement(root, "define")
        ET.SubElement(root, "materials")

        solids = ET.SubElement(root, "solids")
        ET.SubElement(solids, "box", {
            "name": "solidWorld",
            "x": utils.to_mm_str(100),
            "y": utils.to_mm_str(100),
            "z": utils.to_mm_str(100),
            "lunit": "mm"
        })

        structure = ET.SubElement(root, "structure")
        vol = ET.SubElement(structure, "volume", {"name": "logicWorld"})
        ET.SubElement(vol, "materialref", {"ref": "G4_Galactic"})
        ET.SubElement(vol, "solidref", {"ref": "solidWorld"})

        setup = ET.SubElement(root, "setup", {"name": "Default", "version": "1.0"})
        ET.SubElement(setup, "world", {"ref": "logicWorld"})

        return self._prettify_xml(root)

    @staticmethod
    def _prettify_xml(root: ET.Element) -> str:
        """Return a pretty-printed XML string for a given ElementTree root."""
        xml_bytes = ET.tostring(root, "utf-8")
        pretty = parseString(xml_bytes).toprettyxml(indent="  ")
        no_decl = "\n".join(pretty.split("\n")[1:])
        return '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + no_decl
