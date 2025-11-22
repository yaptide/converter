import xml.etree.ElementTree as ET

class MaterialCollector:
    @staticmethod
    def collect(node, acc):
        mat = node.get("simulationMaterial", {}).get("geant4_name")
        if mat:
            acc.add(mat)
        for ch in node.get("children", []):
            MaterialCollector.collect(ch, acc)


class MaterialEmitter:
    @staticmethod
    def emit(materials_xml, used):
        if "BlackHole" in used:
            mat = ET.SubElement(materials_xml, "material",
                                {"name": "BlackHole", "state": "solid"})
            ET.SubElement(mat, "T", {"unit": "K", "value": "293.15"})
            ET.SubElement(mat, "MEE", {"unit": "eV", "value": "823"})
            ET.SubElement(mat, "D", {"unit": "g/cm3", "value": "1e+8"})
            ET.SubElement(mat, "fraction", {"n": "1", "ref": "G4_Pb"})