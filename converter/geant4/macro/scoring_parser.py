from typing import Dict, Any, List
import converter.geant4.utils as utils
from converter.geant4.constants import GEANT4_PARTICLE_MAP, GEANT4_QUANTITY_MAP, GEANT4_KINETIC_ENERGY_SPECTRUM


def generate_scoring_lines(
    data: Dict[str, Any]
) -> tuple[List[str], List[Dict[str, Any]]]:
    """Generate Scoring commands based on configuration."""
    lines: List[str] = [
        "\n##########################################",
        "################ Scoring #################",
        "##########################################\n",
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
            det_lines, det_probes = build_detector_scoring_lines(detector, quantities, filters)
            lines.extend(det_lines)
            probe_histograms.extend(det_probes)

    return lines, probe_histograms


def build_detector_scoring_lines(
    detector: Dict[str, Any],
    quantities: List[Dict[str, Any]],
    filters: Dict[str, Dict[str, Any]],
) -> tuple[List[str], List[Dict[str, Any]]]:
    """Build all scoring lines for a single detector."""
    lines: List[str] = []
    probe_histograms: List[Dict[str, Any]] = []

    name = utils.get_detector_name(detector)
    geom = detector.get("geometryData", {})
    geom_type = geom.get("geometryType", "Box")
    params = geom.get("parameters", {})
    pos_det = geom.get("position", [0, 0, 0])

    is_probe = any(q.get("keyword") == GEANT4_KINETIC_ENERGY_SPECTRUM for q in quantities)
    if is_probe:
        lines.extend(build_probe_lines(detector, geom_type, params, pos_det))
    else:
        lines.extend(build_mesh_lines(detector, geom_type, params, pos_det))

    for quantity in quantities:
        q_lines, q_probes = build_quantity_lines(quantity, filters, name)
        lines.extend(q_lines)
        probe_histograms.extend(q_probes)

    lines.append("/score/close\n")

    return lines, probe_histograms


def build_mesh_lines(
    detector: Dict[str, Any],
    geom_type: str,
    params: Dict[str, Any],
    pos_det: List[float],
) -> List[str]:
    """Build mesh-type scoring detector definition."""
    lines: List[str] = []
    name = utils.get_detector_name(detector)

    if geom_type.lower() in ["cyl", "cylinder"]:
        radius = params.get("radius", 1)
        depth = params.get("depth", 1)
        n_radial = params.get("radialSegments", 1)
        n_z = params.get("zSegments", 1)

        lines.extend([
            f"/score/create/cylinderMesh {name}",
            f"/score/mesh/translate/xyz {pos_det[0]} {pos_det[1]} {pos_det[2]} cm",
            f"/score/mesh/cylinderSize {radius} {depth / 2} cm",
            f"/score/mesh/nBin {n_radial} {n_z} 1",
        ])
    else:
        width = params.get("width", 1)
        height = params.get("height", 1)
        depth = params.get("depth", 1)
        n_x = params.get("xSegments", 1)
        n_y = params.get("ySegments", 1)
        n_z = params.get("zSegments", 1)

        lines.extend([
            f"/score/create/boxMesh {name}",
            f"/score/mesh/translate/xyz {pos_det[0]} {pos_det[1]} {pos_det[2]} cm",
            f"/score/mesh/boxSize {width / 2} {height / 2} {depth / 2} cm",
            f"/score/mesh/nBin {n_x} {n_y} {n_z}",
        ])

    return lines


def build_probe_lines(
    detector: Dict[str, Any],
    geom_type: str,
    params: Dict[str, Any],
    pos_det: List[float],
) -> List[str]:
    """Build probe-type detector scoring definition."""
    name = utils.get_detector_name(detector)
    size = params.get("radius", 1) if geom_type.lower() in ["cyl", "cylinder"] \
        else max(params.get("width", 1), params.get("height", 1), params.get("depth", 1))

    return [
        f"/score/create/probe {name} {size / 2} cm",
        f"/score/probe/locate {pos_det[0]} {pos_det[1]} {pos_det[2]} cm",
    ]


def build_quantity_lines(
    quantity: Dict[str, Any],
    filters: Dict[str, Dict[str, Any]],
    detector_name: str,
) -> tuple[List[str], List[Dict[str, Any]]]:
    """Build scoring quantity definition lines."""
    lines: List[str] = []
    probe_histograms: List[Dict[str, Any]] = []

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
            particle_names = " ".join(pm["name"] for pm in particles_metadata)
            lines.append(f"/score/filter/particle {filter_particles['name']} {particle_names}")

    return lines, probe_histograms
