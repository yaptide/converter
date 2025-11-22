# skipcq: BAN-B405
import xml.etree.ElementTree as ET


class MaterialCollector:
    """Recursively collects all unique GEANT4 material names from geometry nodes."""

    @staticmethod
    def collect(node, acc):
        """Collect material names appearing in geometry nodes."""
        mat = node.get("simulationMaterial", {}).get("geant4_name")
        if mat:
            acc.add(mat)
        for ch in node.get("children", []):
            MaterialCollector.collect(ch, acc)


class MaterialEmitter:
    """Generates the <materials> section of a GDML file."""

    @staticmethod
    def emit(materials_xml, used):
        """if BlackHole is in materials add it to GDML file"""
        if "BlackHole" in used:
            mat = ET.SubElement(materials_xml, "material",
                                {"name": "BlackHole", "state": "solid"})
            ET.SubElement(mat, "T", {"unit": "K", "value": "293.15"})
            ET.SubElement(mat, "MEE", {"unit": "eV", "value": "823"})
            ET.SubElement(mat, "D", {"unit": "g/cm3", "value": "1e+8"})
            ET.SubElement(mat, "fraction", {"n": "1", "ref": "G4_Pb"})
