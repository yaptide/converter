# skipcq: BAN-B405
import xml.etree.ElementTree as ET
from converter.geant4 import utils


def create_solid_element(node: dict, solid_name: str) -> ET.Element | None:
    """Create and return a GDML <solid> element for a given geometry node."""
    geo = node.get("geometryData", {})
    geom_type = geo.get("geometryType")
    params = geo.get("parameters", {})

    if geom_type in ("HollowCylinderGeometry", "CylinderGeometry"):
        return ET.Element("tube", {
            "name": solid_name,
            "rmin": utils.to_mm_str(float(params.get("innerRadius", 0))),
            "rmax": utils.to_mm_str(float(params.get("radius", 0))),
            "z": utils.to_mm_str(float(params.get("depth", 0))),
            "startphi": "0",
            "deltaphi": "360",
            "aunit": "deg",
            "lunit": "mm",
        })

    elif geom_type == "SphereGeometry":
        return ET.Element("sphere", {
            "name": solid_name,
            "rmin": "0",
            "rmax": utils.to_mm_str(float(params.get("radius", 0))),
            "startphi": "0",
            "deltaphi": "360",
            "starttheta": "0",
            "deltatheta": "180",
            "aunit": "deg",
            "lunit": "mm",
        })

    elif geom_type == "BoxGeometry":
        return ET.Element("box", {
            "name": solid_name,
            "x": utils.to_mm_str(float(params.get("width", 0))),
            "y": utils.to_mm_str(float(params.get("height", 0))),
            "z": utils.to_mm_str(float(params.get("depth", 0))),
            "lunit": "mm",
        })

    return None
