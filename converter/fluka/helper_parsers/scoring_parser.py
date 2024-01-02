from dataclasses import dataclass
from typing import Optional, Union

from converter.fluka.helper_parsers.detector_parser import Detector, parse_detector

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

_particle_mappings = map[str, str] = {
    'Neutron': 'NEUTRON',
    'Proton': 'PROTON',
    'Pion π-': 'PION-',
    'Pion π+': 'PION+',
    'Anti-neutron': 'ANEUTRON',
    'Anti-proton': 'APROTON',
    'Kaon κ-': 'KAON-',
    'Kaon κ+': 'KAON+',
    'Kaon κ0': 'KAONZERO',
    'Kaon κ~': 'AKAONZER',
    'Muon µ-': 'MUON-',
    'Muon µ+': 'MUON+',
    'Deuteron': 'DEUTERON',
    'Triton': 'TRITON',
    'Helium-3': 'HELIUM3',
    'Helium-4': 'HELIUM4',
    'Heavy ions': 'HEAVYION',
}

__supported_filter_keywords = 'A', 'Z'


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
    filter: Optional[Union[CustomFilter, ParticleFilter]]
    modifiers: list[any]  # unused
    keyword: str = 'DOSE'


@dataclass
class Scoring:
    """Class representing Scorings for Fluka output"""

    output_unit: int
    quantities: list[Quantity]
    detector: Detector


def get_particle_filter(filter_dict: dict) -> Optional[ParticleFilter]:
    """Creates ParticleFilter from dictionary.

    Returns None if filter cannot be created for Fluka.
    """
    particle = filter_dict['particle']
    if particle.get('name') not in _particle_mappings:
        return None

    return ParticleFilter(name=particle['name'], id=filter_dict['uuid'], particle=_particle_mappings[particle['name']])


def get_custom_filter(filter_dict: dict) -> list[CustomFilter]:
    """Creates CustomFilter from dictionary.

    Returns None if filter cannot be created for Fluka.
    """
    if not filter_dict.get('rules'):
        return None
    else:
        a = 0
        z = 0
        for rule in filter_dict['rules']:
            if rule['keyword'] not in __supported_filter_keywords:
                return None
            if rule['operator'] != '==':
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
    else:
        return get_custom_filter(filter_dict)


def parse_scorings(detectors_json: dict, scorings_json: dict) -> list[Scoring]:
    """Creates list of Scorings from dictionaries"""
    filters: map[str, Union[ParticleFilter, CustomFilter]] = {}
    for filter_dict in scorings_json['filters']:
        # Check if supported filter, ignore otherwise
        filter = get_filter(filter_dict)
        if filter is not None:
            filters[filter_dict['uuid']] = filter

    # Iterate over outputs and create cards for quantities
    # Quantity can use filters (e.g. energy, particle type)
    default_output_unit = 21
    outputs: list[Scoring] = []
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
            filter_dict = quantity.get('filter')
            # if filter_dict is not None:
            #     if filter_dict.get("particle"):
            #         filter_dict = get_particle_filter(filter_dict)
            #     else:
            #         rules: list[FilterRule] = filter_filter_by_its_rules(dict(filter_dict['rules'])
            #         filter = CustomFilter(name=filter['name'], rules=rules)
            quantities.append(
                Quantity(name=quantity['name'],
                         keyword=quantity['keyword'],
                         filter=filter,
                         modifiers=quantity.get('modifiers')))
        output = Scoring(default_output_unit, [], parse_detector(output))
        if detector['geometryData']['geometryType'] != 'Mesh':
            continue

        scorings.append(Scoring(detectorUuid=detector['uuid'], name=detector['name'],
                                detector=parse_detector(detector)))

    return scorings
