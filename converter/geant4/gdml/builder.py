
from typing import Dict, Tuple, Optional, Set
import xml.etree.ElementTree as ET
from defusedxml.minidom import parseString
import converter.geant4.utils as utils


class Geant4GDMLBuilder:
    """Generates GDML geometry trees from JSON geometry nodes."""

    def __init__(self, world_json: Optional[dict]):
        self.world_json = world_json

    def generate(self) -> str:
        if self.world_json:
            return self._generate_gdml(self.world_json)
        return self._generate_empty()

    # -------------------- MAIN -----------------------

    def _generate_gdml(self, world: dict) -> str:
        gdml_root = ET.Element("gdml", {
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:noNamespaceSchemaLocation": "http://cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd",
        })

        ET.SubElement(gdml_root, "define")

        used_materials: Set[str] = set()
        self._collect_materials(world, used_materials)

        materials_xml = ET.SubElement(gdml_root, "materials")
        self._emit_materials(materials_xml, used_materials)

        solids_xml = ET.SubElement(gdml_root, "solids")
        structure_xml = ET.SubElement(gdml_root, "structure")

        name_counters = {"solid": {}, "logic": {}, "phys": {}}

        self._emit_node_postorder(world, solids_xml, structure_xml, name_counters)

        setup_xml = ET.SubElement(gdml_root, "setup", {"name": "Default", "version": "1.0"})
        ET.SubElement(setup_xml, "world", {"ref": utils.choose_logic_name(world)})

        return self._prettify_xml(gdml_root)

    # ---------------- EMPTY WORLD --------------------

    def _generate_empty(self) -> str:
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

    # ---------------- MATERIALS ----------------------

    def _emit_materials(self, materials_xml: ET.Element, used: Set[str]):
        if "BlackHole" in used:
            mat = ET.SubElement(materials_xml, "material", {"name": "BlackHole", "state": "solid"})
            ET.SubElement(mat, "T", {"unit": "K", "value": "293.15"})
            ET.SubElement(mat, "MEE", {"unit": "eV", "value": "823"})
            ET.SubElement(mat, "D", {"unit": "g/cm3", "value": "1e+8"})
            ET.SubElement(mat, "fraction", {"n": "1", "ref": "G4_Pb"})

    def _collect_materials(self, node: dict, acc: Set[str]) -> None:
        mat = node.get("simulationMaterial", {}).get("geant4_name")
        if mat:
            acc.add(mat)
        for ch in node.get("children", []):
            self._collect_materials(ch, acc)

    # ---------------- NODES (SOLIDS + STRUCTURE) -----

    def _emit_node_postorder(
        self,
        node: dict,
        solids_xml: ET.Element,
        structure_xml: ET.Element,
        counters: Dict[str, Dict[str, int]],
    ) -> Tuple[str, str]:

        # recurse
        children = []
        for ch in node.get("children", []):
            ch_logic, _ = self._emit_node_postorder(ch, solids_xml, structure_xml, counters)
            pos = ch.get("geometryData", {}).get("position", [0,0,0])
            children.append((ch, ch_logic, pos))

        # SOLID
        solid_name = utils.choose_solid_name(node, counters)
        self._emit_solid(node, solids_xml, solid_name)

        # LOGICAL VOLUME
        logic_name = utils.choose_logic_name(node, counters)
        vol = ET.SubElement(structure_xml, "volume", {"name": logic_name})

        mat = node.get("simulationMaterial", {}).get("geant4_name", "G4_Galactic")
        ET.SubElement(vol, "materialref", {"ref": mat})
        ET.SubElement(vol, "solidref", {"ref": solid_name})

        # PHYSICAL VOLUMES
        for (child, child_logic, pos) in children:
            phys_name = utils.choose_phys_name(child, counters)
            phys = ET.SubElement(vol, "physvol", {"copynumber": "1", "name": phys_name})
            ET.SubElement(phys, "volumeref", {"ref": child_logic})

            x,y,z = pos
            if abs(x)>utils.EPS or abs(y)>utils.EPS or abs(z)>utils.EPS:
                ET.SubElement(phys, "position", {
                    "name": f"{phys_name}_pos",
                    "unit": "mm",
                    "x": utils.to_mm_str(x),
                    "y": utils.to_mm_str(y),
                    "z": utils.to_mm_str(z),
                })

        return logic_name, solid_name

    # ---------------- SOLID TYPES --------------------

    def _emit_solid(self, node, solids_xml, solid_name):
        geo = node.get("geometryData", {})
        geom_type = geo.get("geometryType")
        params = geo.get("parameters", {})

        if geom_type in ("HollowCylinderGeometry","CylinderGeometry"):
            ET.SubElement(solids_xml, "tube", {
                "name": solid_name,
                "rmin": utils.to_mm_str(float(params.get("innerRadius", 0))),
                "rmax": utils.to_mm_str(float(params.get("radius", 0))),
                "z": utils.to_mm_str(float(params.get("depth", 0))),
                "startphi": "0", "deltaphi": "360",
                "aunit": "deg", "lunit": "mm"
            })

        elif geom_type == "SphereGeometry":
            ET.SubElement(solids_xml, "sphere", {
                "name": solid_name,
                "rmin": "0",
                "rmax": utils.to_mm_str(float(params.get("radius", 0))),
                "startphi": "0", "deltaphi": "360",
                "starttheta": "0", "deltatheta": "180",
                "aunit": "deg", "lunit": "mm"
            })

        elif geom_type == "BoxGeometry":
            ET.SubElement(solids_xml, "box", {
                "name": solid_name,
                "x": utils.to_mm_str(float(params.get("width", 0))),
                "y": utils.to_mm_str(float(params.get("height", 0))),
                "z": utils.to_mm_str(float(params.get("depth", 0))),
                "lunit": "mm"
            })

    # ---------------- PRETTY PRINT -------------------

    @staticmethod
    def _prettify_xml(root: ET.Element) -> str:
        xml_bytes = ET.tostring(root, "utf-8")
        pretty = parseString(xml_bytes).toprettyxml(indent="  ")
        no_decl = "\n".join(pretty.split("\n")[1:])
        return '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + no_decl