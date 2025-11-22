from typing import Dict, Any, List
from converter.geant4 import utils


class ResultParser:
    """Generate results section (dump to file)."""

    def __init__(self, data: Dict[str, Any], lines: List[str]):
        self.data = data
        self.lines = lines

    def parse(self):
        """Generate commands for writing scoring results to output files."""
        detectors = {d["uuid"]: d for d in self.data.get("detectorManager", {}).get("detectors", [])}
        outputs = self.data.get("scoringManager", {}).get("outputs", [])

        self.lines.extend([
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
                self.lines.append(f"/score/dumpQuantityToFile {name} {qname} {filename}")
