from dataclasses import dataclass, field
from converter.fluka.cards.card import Card

from converter.fluka.helper_parsers.detector_parser import MeshDetector


@dataclass
class Scoring:
    """Class representing single Scoring in Fluka"""

    detectorUuid: str
    name: str
    output_unit: int
    quantity: str

    def __str__(self) -> str:
        """Returns string representation of Scoring card"""
        raise NotImplementedError('Scoring handler not implemented')


@dataclass
class UsrbinCartesianScoring(Scoring):
    """Class representing USRBIN Cartesian Scoring in Fluka"""
    detector: MeshDetector

    def __str__(self) -> str:
        """Returns string representation of USRBIN for cartesian scoring card"""
        first_card = self._handle_first_card()
        second_card = self._handle_second_card()

        return f'{first_card!s}\n{second_card!s}\n'

    def _handle_first_card(self) -> Card:
        """Creates first Scoring card"""

        # Probably we should add some kind of mapping here or when creating cards
        particle_of_scoring = self.quantity
        output_unit = str(self.output_unit * -1)

        what = ['10.0', particle_of_scoring, output_unit, self.detector.x_max, self.detector.y_max, self.detector.z_max]

        return Card(codewd='USRBIN', what=what, sdum='changeme')

    def _handle_second_card(self) -> Card:
        """Creates second Scoring card"""
        what = [
            self.detector.x_min,
            self.detector.y_min,
            self.detector.z_min,
            self.detector.x_bins,
            self.detector.y_bins,
            self.detector.z_bins,
        ]

        return Card(codewd='USRBIN', what=what, sdum='&')


def parse_scorings(detectors_json: dict, scorings_json: dict) -> list[Scoring]:
    """Creates list of Scorings from dictionaries"""
    scorings = []
    for scoring in scorings_json['outputs']:
        detector_dict = next(
            (detector for detector in detectors_json['detectors'] if detector['uuid'] == scoring['detectorUuid']), None)

        if detector_dict and detector_dict['geometryData']['geometryType'] == 'Mesh':
            scorings.append(
                UsrbinCartesianScoring(detectorUuid=scoring['detectorUuid'],
                                       output_unit=21,
                                       quantity='DOSE',
                                       name=scoring['name'],
                                       detector=MeshDetector.parse_mesh_detector(detector_dict)))

    return scorings
