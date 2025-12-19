from typing import Dict, List
import converter.geant4.utils as utils


def generate_result_lines(data: Dict) -> List[str]:
    """Generate commands for writing scoring results to output files."""
    lines: List[str] = []
    detectors = {d["uuid"]: d for d in data.get("detectorManager", {}).get("detectors", [])}
    outputs = data.get("scoringManager", {}).get("outputs", [])

    lines.extend([
        "##########################################",
        "############ Collect results #############",
        "##########################################\n"
    ])

    for output in outputs:
        detector_uuid = output.get("detectorUuid")
        detector = detectors.get(detector_uuid)
        if not detector:
            continue
        name = utils.get_detector_name(detector)
        for quantity in output.get("quantities", []):
            qname = quantity.get("name", quantity.get("keyword", "UnknownQuantity"))
            filename = f"{name}_{qname}.txt"
            lines.append(f"/score/dumpQuantityToFile {name} {qname} {filename}")

    return lines
