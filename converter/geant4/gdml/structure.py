# skipcq: BAN-B405
import xml.etree.ElementTree as ET
from converter.geant4 import utils
from .solids import SolidEmitter


class StructureEmitter:
    """Generates the <structure> section of a GDML file."""

    def __init__(self, solids_xml, structure_xml, counters):
        self.solids_xml = solids_xml
        self.structure_xml = structure_xml
        self.counters = counters

    def emit(self, node):
        """Recursively emit GDML solids and structure definitions for a node and its children"""
        children = []
        for ch in node.get("children", []):
            logic_name, _ = self.emit(ch)
            pos = ch.get("geometryData", {}).get("position", [0, 0, 0])
            children.append((ch, logic_name, pos))

        solid_name = utils.choose_solid_name(node, self.counters)
        SolidEmitter.emit(node, self.solids_xml, solid_name)

        logic_name = utils.choose_logic_name(node, self.counters)
        vol = ET.SubElement(self.structure_xml, "volume", {"name": logic_name})

        material_name = node.get("simulationMaterial", {}).get("geant4_name", "G4_Galactic")
        ET.SubElement(vol, "materialref", {"ref": material_name})
        ET.SubElement(vol, "solidref", {"ref": solid_name})

        for (child, child_logic, pos) in children:
            phys_name = utils.choose_phys_name(child, self.counters)
            phys = ET.SubElement(vol, "physvol", {"copynumber": "1", "name": phys_name})
            ET.SubElement(phys, "volumeref", {"ref": child_logic})

            x, y, z = pos
            if abs(x) > utils.EPS or abs(y) > utils.EPS or abs(z) > utils.EPS:
                ET.SubElement(phys, "position", {
                    "name": f"{phys_name}_pos",
                    "unit": "mm",
                    "x": utils.to_mm_str(x),
                    "y": utils.to_mm_str(y),
                    "z": utils.to_mm_str(z),
                })

        return logic_name, solid_name
