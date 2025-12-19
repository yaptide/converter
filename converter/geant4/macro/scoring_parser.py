from typing import Dict, Any, List
import converter.geant4.utils as utils
from converter.geant4.constants import GEANT4_PARTICLE_MAP, GEANT4_QUANTITY_MAP, GEANT4_KINETIC_ENERGY_SPECTRUM


def generate_scoring_lines(data: Dict[str, Any]) -> (List[str], List[Dict[str, Any]]):
    """Generate Scoring commands based on configuration."""
    lines: List[str] = [
        "\n##########################################",
        "################ Scoring #################",
        "##########################################\n"
    ]
    probe_histograms: List[Dict[str, Any]] = []

    detectors = {d["uuid"]: d for d in data.get("detectorManager", {}).get("detectors", [])}
    outputs = data.get("scoringManager", {}).get("outputs", [])
    filters = {f["uuid"]: f for f in data.get("scoringManager", {}).get("filters", [])}

    detector_quantities: Dict[str, List[Dict[str, Any]]] = {}
    for output in outputs:
        detector_uuid = output.get("detectorUuid")
        detector_quantities.setdefault(detector_uuid, []).extend(output.get("quantities", []))

    for detector_uuid, quantities in detector_quantities.items():
        detector = detectors.get(detector_uuid)
        if detector:
            _append_detector_scoring_lines(detector, quantities, filters, lines, probe_histograms)

    return lines, probe_histograms


def _append_detector_scoring_lines(detector, quantities, filters, lines, probe_histograms):
    """Append all scoring quantities and filters for a given detector."""
    name = utils.get_detector_name(detector)
    geom = detector.get("geometryData", {})
    geom_type = geom.get("geometryType", "Box")
    params = geom.get("parameters", {})
    pos_det = geom.get("position", [0, 0, 0])

    is_probe = any(q.get("keyword") == GEANT4_KINETIC_ENERGY_SPECTRUM for q in quantities)
    if is_probe:
        _append_probe_lines(detector, geom_type, params, pos_det, lines)
    else:
        _append_mesh_lines(detector, geom_type, params, pos_det, lines)

    for quantity in quantities:
        _append_quantity_lines(quantity, filters, name, lines, probe_histograms)

    lines.append("/score/close\n")


def _append_mesh_lines(detector, geom_type, params, pos_det, lines):
    """Append a mesh-type scoring detector definition to the macro."""
    name = utils.get_detector_name(detector)
    if geom_type.lower() in ["cyl", "cylinder"]:
        lines.append(f"/score/create/cylinderMesh {name}")
        lines.append(f"/score/mesh/translate/xyz {pos_det[0]} {pos_det[1]} {pos_det[2]} cm")
        radius = params.get("radius", 1)
        depth = params.get("depth", 1)
        n_radial = params.get("radialSegments", 1)
        n_z = params.get("zSegments", 1)
        lines.append(f"/score/mesh/cylinderSize {radius} {depth / 2} cm")
        lines.append(f"/score/mesh/nBin {n_radial} {n_z} 1")
    else:
        lines.append(f"/score/create/boxMesh {name}")
        lines.append(f"/score/mesh/translate/xyz {pos_det[0]} {pos_det[1]} {pos_det[2]} cm")
        width = params.get("width", 1)
        height = params.get("height", 1)
        depth = params.get("depth", 1)
        n_x = params.get("xSegments", 1)
        n_y = params.get("ySegments", 1)
        n_z = params.get("zSegments", 1)
        lines.append(f"/score/mesh/boxSize {width / 2} {height / 2} {depth / 2} cm")
        lines.append(f"/score/mesh/nBin {n_x} {n_y} {n_z}")


def _append_probe_lines(detector, geom_type, params, pos_det, lines):
    """Append a probe-type detector scoring definition to the macro."""
    name = utils.get_detector_name(detector)
    size = params.get("radius", 1) if geom_type.lower() in ["cyl", "cylinder"] \
        else max(params.get("width", 1), params.get("height", 1), params.get("depth", 1))
    lines.append(f"/score/create/probe {name} {size / 2} cm")
    lines.append(f"/score/probe/locate {pos_det[0]} {pos_det[1]} {pos_det[2]} cm")


def _append_quantity_lines(quantity, filters, detector_name, lines, probe_histograms):
    """Append a scoring quantity definition to the macro."""
    keyword = quantity.get("keyword", "")
    qname = quantity.get("name", keyword)
    mapped_keyword = GEANT4_QUANTITY_MAP.get(keyword, keyword.lower())
    lines.append(f"/score/quantity/{mapped_keyword} {qname}")

    if keyword == GEANT4_KINETIC_ENERGY_SPECTRUM:
        probe_histograms.append({
            "quantity": qname,
            "detector": detector_name,
            "bins": quantity.get("histogramNBins", 1),
            "min": quantity.get("histogramMin", 0),
            "max": quantity.get("histogramMax", 1),
            "unit": quantity.get("histogramUnit", "MeV"),
            "XScale": quantity.get("histogramXScale", "none"),
            "XBinScheme": quantity.get("histogramXBinScheme", "linear"),
        })

    filter_uuid = quantity.get("filter")
    if filter_uuid and filter_uuid in filters:
        filter_particles = filters[filter_uuid]
        particle_types = filter_particles.get("data", {}).get("particleTypes", [])
        if particle_types:
            particles_metadata = [GEANT4_PARTICLE_MAP.get(pt["id"]) for pt in particle_types]
            particles_metadata = filter(lambda x: x is not None, particles_metadata)
            particle_names = " ".join([pm["name"] for pm in particles_metadata])
            lines.append(f"/score/filter/particle {filter_particles['name']} {particle_names}")
