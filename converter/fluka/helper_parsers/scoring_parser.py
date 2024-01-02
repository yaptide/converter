from dataclasses import dataclass

from converter.fluka.helper_parsers.detector_parser import Detector, parse_detector


@dataclass
class Scoring:
    """Class representing Scoring"""

    detectorUuid: str
    detector: Detector
    name: str = ''
    quantity: str = 'DOSE'


# def parse_scorings(detectors_json: dict, scorings_json: dict) -> list[Scoring]:
#     """Creates list of Scorings from dictionaries"""
#     scorings = []
#     for scoring in scorings_json['outputs']:
#         detector = next(
#             (detector for detector in detectors_json['detectors'] if detector['uuid'] == scoring['detectorUuid']),
#             None
#         )

#         if detector['geometryData']['geometryType'] != "Mesh":
#             continue

#         scorings.append(
#             Scoring(
#                 detectorUuid=scoring['detectorUuid'],
#                 name=scoring['name'],
#                 detector=parse_detector(detector)
#             )
#         )

#     return scorings
