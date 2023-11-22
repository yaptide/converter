from dataclasses import dataclass, field
from converter.fluka.helper_parsers.detector_parser import USRBIN


@dataclass
class Detector:
    name: str = ""

@dataclass
class Scoring:

    detectorUuid: str
    name: str = ""
    quantity: str = "DOSE"


def parse_scorings(detectors_json: dict, scorings_json: dict) -> list[Scoring]:
    print("Test")

    scorings = []
    for scoring in scorings_json['outputs']:
        scorings.append(
            Scoring(
                detectorUuid=scoring['detectorUuid'],
                name=scoring['name'],
                quantity="DOSE"
            )
        )

    return scorings