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
        scorings.append(
            Scoring(
                detectorUuid=scoring['detectorUuid'],
                name=scoring['name'],
                detector=parse_detector(detectors_json, scoring['detectorUuid'])
            )
        )

    return scorings
