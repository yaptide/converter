
from converter.common import Parser
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, Tuple, Optional, Set

_MM_PER_CM = 10.0

def _to_mm_str(val_cm: float) -> str:
    mm = val_cm * _MM_PER_CM
    if abs(mm - int(mm)) < 1e-9:
        return str(int(mm))
    return f"{mm:g}"

def _pascal(s: str) -> str:
    return "".join(part.capitalize() for part in s.replace("_", " ").split())

class Geant4Parser(Parser):

    def __init__(self) -> None:
        super().__init__()
        self.info["simulator"] = "geant4"
        self._gdml_content: str = ""


    def parse_configs(self, json_data: dict) -> None:
        if "figureManager" in json_data and json_data["figureManager"]["figures"]:
            world_figure_json = json_data["figureManager"]["figures"][0]
            self._gdml_content = self._generate_gdml(world_figure_json)
        else:
            self._gdml_content = self._generate_empty_gdml()

    def get_configs_json(self) -> dict:
        return {"geometry.gdml": self._gdml_content}


    def _generate_gdml(self, world: dict) -> str:
        gdml_root = ET.Element("gdml", {
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:noNamespaceSchemaLocation": "http://cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd",
        })

        ET.SubElement(gdml_root, "define")
        used_materials: Set[str] = set()
        self._collect_materials(world, used_materials)

        materials_xml = ET.SubElement(gdml_root, "materials")
        if "BlackHole" in used_materials:
            mat = ET.SubElement(materials_xml, "material", {"name": "BlackHole", "state": "solid"})
            ET.SubElement(mat, "T", {"unit": "K", "value": "293.15"})
            ET.SubElement(mat, "MEE", {"unit": "eV", "value": "823"})
            ET.SubElement(mat, "D", {"unit": "g/cm3", "value": "1e+8"})
            ET.SubElement(mat, "fraction", {"n": "1", "ref": "G4_Pb"})

        solids_xml = ET.SubElement(gdml_root, "solids")
        structure_xml = ET.SubElement(gdml_root, "structure")
        name_counters = {"solid": {}, "logic": {}, "phys": {}}

        self._emit_node_postorder(world, solids_xml, structure_xml, name_counters)

        setup_xml = ET.SubElement(gdml_root, "setup", {"name": "Default", "version": "1.0"})
        world_logic_name = self._choose_logic_name(world)
        ET.SubElement(setup_xml, "world", {"ref": world_logic_name})

        xml_bytes = ET.tostring(gdml_root, "utf-8")
        pretty = minidom.parseString(xml_bytes).toprettyxml(indent="  ")
        pretty_no_decl = "\n".join(pretty.split("\n")[1:])
        return '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n' + pretty_no_decl

    def _generate_empty_gdml(self) -> str:
        root = ET.Element("gdml", {
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:noNamespaceSchemaLocation": "http://cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd",
        })
        ET.SubElement(root, "define")
        ET.SubElement(root, "materials")
        solids = ET.SubElement(root, "solids")
        ET.SubElement(solids, "box", {
            "name": "solidWorld", "x": _to_mm_str(100), "y": _to_mm_str(100), "z": _to_mm_str(100), "lunit": "mm"
        })
        structure = ET.SubElement(root, "structure")
        vol = ET.SubElement(structure, "volume", {"name": "logicWorld"})
        ET.SubElement(vol, "materialref", {"ref": "G4_Galactic"})
        ET.SubElement(vol, "solidref", {"ref": "solidWorld"})
        setup = ET.SubElement(root, "setup", {"name": "Default", "version": "1.0"})
        ET.SubElement(setup, "world", {"ref": "logicWorld"})

        xml_bytes = ET.tostring(root, "utf-8")
        pretty = minidom.parseString(xml_bytes).toprettyxml(indent="  ")
        pretty_no_decl = "\n".join(pretty.split("\n")[1:])
        return '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n' + pretty_no_decl


    def _collect_materials(self, node: dict, acc: Set[str]) -> None:
        mat = node.get("simulationMaterial", {})
        g4 = mat.get("geant4_name")
        if g4:
            acc.add(g4)
        for ch in node.get("children", []):
            self._collect_materials(ch, acc)

    def _unique_name(self, base: str, kind: str, counters: Dict[str, Dict[str, int]]) -> str:
        used = counters[kind]
        if base not in used:
            used[base] = 1
            return base
        used[base] += 1
        return f"{base}{used[base]}"

    def _choose_solid_name(self, node: dict, counters: Dict[str, Dict[str, int]]) -> str:
        return self._unique_name(f"solid{_pascal(node.get('name','Figure'))}", "solid", counters)

    def _choose_logic_name(self, node: dict, counters: Optional[Dict[str, Dict[str, int]]] = None) -> str:
        if counters is None:
            return f"logic{_pascal(node.get('name','Figure'))}"
        return self._unique_name(f"logic{_pascal(node.get('name','Figure'))}", "logic", counters)

    def _choose_phys_name(self, child_node: dict, counters: Dict[str, Dict[str, int]]) -> str:
        return self._unique_name(f"phys{_pascal(child_node.get('name','Figure'))}", "phys", counters)

    def _emit_node_postorder(
        self,
        node: dict,
        solids_xml: ET.Element,
        structure_xml: ET.Element,
        name_counters: Dict[str, Dict[str, int]],
    ) -> Tuple[str, str]:
        geo = node.get("geometryData", {})
        params = geo.get("parameters", {})
        geom_type = geo.get("geometryType")
        children_info = []
        for ch in node.get("children", []):
            ch_logic_name, _ = self._emit_node_postorder(ch, solids_xml, structure_xml, name_counters)
            children_info.append((ch, ch_logic_name, ch.get("geometryData", {}).get("position", [0, 0, 0])))

        solid_name = self._choose_solid_name(node, name_counters)
        if geom_type ==  ("HollowCylinderGeometry", "CylinderGeometry") :
            rmin_cm = float(params.get("innerRadius", 0))
            rmax_cm = float(params.get("radius", 0))
            z_cm = float(params.get("depth", 0))
            ET.SubElement(solids_xml, "tube", {
                "name": solid_name,
                "rmin": _to_mm_str(rmin_cm),
                "rmax": _to_mm_str(rmax_cm),
                "z": _to_mm_str(z_cm),
                "startphi": "0", "deltaphi": "360",
                "aunit": "deg", "lunit": "mm"
            })
        elif geom_type == "SphereGeometry":
            r_cm = float(params.get("radius", 0))
            ET.SubElement(solids_xml, "sphere", {
                "name": solid_name,
                "rmin": "0",
                "rmax": _to_mm_str(r_cm),
                "startphi": "0",
                "deltaphi": "360",
                "starttheta": "0",
                "deltatheta": "180",
                "aunit": "deg",
                "lunit": "mm"
            })
        elif geom_type == "BoxGeometry":
            ET.SubElement(solids_xml, "box", {
                "name": solid_name,
                "x": _to_mm_str(float(params.get("width",0))),
                "y": _to_mm_str(float(params.get("height",0))),
                "z": _to_mm_str(float(params.get("depth",0))),
                "lunit": "mm"
            })

        logic_name = self._choose_logic_name(node, name_counters)
        vol = ET.SubElement(structure_xml, "volume", {"name": logic_name})
        material_name = node.get("simulationMaterial", {}).get("geant4_name", "G4_Galactic")
        ET.SubElement(vol, "materialref", {"ref": material_name})
        ET.SubElement(vol, "solidref", {"ref": solid_name})

        for (child_node, child_logic_name, child_pos_cm) in children_info:
            phys_name = self._choose_phys_name(child_node, name_counters)
            phys = ET.SubElement(vol, "physvol", {"copynumber": "1", "name": phys_name})
            ET.SubElement(phys, "volumeref", {"ref": child_logic_name})
            x_cm, y_cm, z_cm = map(float, child_pos_cm)
            if abs(x_cm) > 1e-12 or abs(y_cm) > 1e-12 or abs(z_cm) > 1e-12:
                ET.SubElement(phys, "position", {
                    "name": f"{phys_name}_pos",
                    "unit": "mm",
                    "x": _to_mm_str(x_cm),
                    "y": _to_mm_str(y_cm),
                    "z": _to_mm_str(z_cm),
                })

        return logic_name, solid_name
