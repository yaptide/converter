from dataclasses import dataclass
from typing import Optional, Union

from converter.fluka.helper_parsers.detector_parser import Detector, parse_detector
from converter.fluka.helper_parsers.beam_parser import particle_dict

__supported_filter_keywords = ('A', 'Z')


@dataclass
class CustomFilter:
    """Class representing CustomFilter"""

    name: str
    a: int
    z: int


@dataclass
class ParticleFilter:
    """Class representing ParticleFilter"""

    name: str
    particle: str


@dataclass
class Quantity:
    """Class representing Quantity"""

    name: str
    scoring_filter: Optional[Union[CustomFilter, ParticleFilter]]
    modifiers: list[any]  # unused
    keyword: str = 'DOSE'


@dataclass
class Scoring:
    """Class representing Scorings for Fluka output"""

    quantities: list[Quantity]
    detector: Detector
    output_unit: int = 21


def get_particle_filter(filter_dict: dict) -> Optional[ParticleFilter]:
    """Creates ParticleFilter from dictionary.

    Returns None if filter cannot be created for Fluka.
    """
    particle = filter_dict['particle']
    if particle.get('id') not in particle_dict:
        return None

    return ParticleFilter(name=particle['name'], particle=particle_dict[particle['id']]['name'])


def get_custom_filter(filter_dict: dict) -> Optional[CustomFilter]:
    """Creates CustomFilter from dictionary.

    Returns empty list if filter cannot be created for Fluka.
    """
    if not filter_dict.get('rules'):
        return None

    a = 0
    z = 0
    for rule in filter_dict['rules']:
        if rule['keyword'] not in __supported_filter_keywords:
            return None
        if rule['operator'] not in ['equal', '==']:
            return None
        if rule['keyword'] == 'A':
            a = rule['value']
        elif rule['keyword'] == 'Z':
            z = rule['value']
    return CustomFilter(name=filter_dict['name'], a=a, z=z)


def get_filter(filter_dict: dict) -> Optional[Union[ParticleFilter, CustomFilter]]:
    """Creates filter for Fluka.

    Returns None if filter cannot be created for Fluka.
    """
    if filter_dict.get('particle'):
        return get_particle_filter(filter_dict)
    return get_custom_filter(filter_dict)


def parse_scorings(detectors_json: dict, scorings_json: dict) -> list[Scoring]:
    """Creates list of Scorings from dictionaries"""
    filters: dict[str, Union[ParticleFilter, CustomFilter]] = {}
    for filter_dict in scorings_json['filters']:
        # Check if supported filter, ignore otherwise
        scoring_filter = get_filter(filter_dict)
        if scoring_filter is not None:
            filters[filter_dict['uuid']] = scoring_filter

    scorings: list[Scoring] = []
    for output in scorings_json['outputs']:
        detector = next(
            (detector for detector in detectors_json['detectors'] if detector['uuid'] == output['detectorUuid']), None)
        if detector is None:
            # Skip for not existing detector
            # This should not happen
            continue

        if detector['geometryData']['geometryType'] != 'Mesh':
            # Skip not cartesian mesh detectors
            continue

        quantities: list[Quantity] = []
        for quantity in output['quantities']:
            scoring_filter = None
            if 'filter' in quantity:
                scoring_filter = filters.get(quantity['filter'])
                if scoring_filter is None:
                    # Skip for not existing filter or not supported filter
                    continue

            quantities.append(
                Quantity(name=quantity['name'],
                         keyword=quantity['keyword'],
                         scoring_filter=scoring_filter,
                         modifiers=quantity.get('modifiers')))

        scorings.append(Scoring(quantities=quantities, detector=parse_detector(detector)))

    return scorings
