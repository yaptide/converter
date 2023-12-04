from dataclasses import dataclass

from converter.fluka.helper_parsers.detector_parser import Detector, parse_detector


@dataclass
class Scoring:
    detectorUuid: str
    detector: Detector
    name: str = ""
    quantity: str = "DOSE"


def parse_scorings(detectors_json: dict, scorings_json: dict) -> list[Scoring]:
    scorings = []
    for scoring in scorings_json['outputs']:

        detector = next(
            (detector for detector in detectors_json['detectors'] if detector['uuid'] == scoring['detectorUuid']),
            None
        )

        scorings.append(
            Scoring(
                detectorUuid=scoring['detectorUuid'],
                name=scoring['name'],
                detector=parse_detector(detector)
            )
        )

    return scorings
