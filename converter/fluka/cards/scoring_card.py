from dataclasses import dataclass, field
from typing import Optional, Union

from converter.fluka.cards.card import Card
from converter.fluka.helper_parsers.detector_parser import Detector
from converter.fluka.helper_parsers.scoring_parser import CustomFilter, ParticleFilter, Quantity, Scoring


@dataclass
class ScoringCardIndexCounter:
    """Class representing counter for Fluka scoring cards"""

    usrbin_counter: int = 0


def handle_scoring_cards(output_unit: int, scoring: Scoring, counter: ScoringCardIndexCounter) -> str:
    """Creates Scoring cards"""
    output: list[str] = []
    for quantity in scoring.quantities:
        usrbin_card = handle_usrbin_scoring(scoring.detector, quantity, output_unit, counter)
        output.append(usrbin_card)
    return '\n'.join(output).strip()


def short_name(name: str) -> str:
    """Creates short name for fluka card"""
    return name[:10]


def handle_usrbin_scoring(detector: Detector, quantity: Quantity, output_unit, counter: ScoringCardIndexCounter) -> str:
    """Creates USRBIN card"""
    output: list[Card] = []
    # temporary assumption
    binning_what = '10.0'
    # DOSE according to:
    # https://flukafiles.web.cern.ch/manual/chapters/particle_and_material_codes/particles_codes.html
    quantity_to_score = ''
    try_auxscore = False
    if quantity.keyword == 'Dose':
        quantity_to_score = 'DOSE'
        try_auxscore = True
    elif quantity.keyword == 'Fluence':
        if isinstance(quantity.scoring_filter, ParticleFilter):
            # Apply particle from filter if fluency is used
            quantity_to_score = quantity.scoring_filter.particle
        else:
            quantity_to_score = 'ALL-PART'
            if isinstance(quantity.scoring_filter, CustomFilter):
                try_auxscore = True

    if not quantity_to_score:
        return f'* unable to create USRBIN card for {quantity.name[:20]}'

    output_unit_in_fluka_convention = str(output_unit * -1)

    first_card = Card(codewd='USRBIN')
    first_card.what = [
        binning_what, quantity_to_score, output_unit_in_fluka_convention, detector.x_max, detector.y_max, detector.z_max
    ]
    first_card.sdum = short_name(quantity.name)
    output.append(first_card)

    second_card = Card(codewd='USRBIN')
    second_card.what = [
        detector.x_min,
        detector.y_min,
        detector.z_min,
        detector.x_bins,
        detector.y_bins,
        detector.z_bins,
    ]
    second_card.sdum = '&'
    output.append(second_card)

    counter.usrbin_counter += 1
    if try_auxscore and quantity.scoring_filter:
        # Add AUXSCORE card for custom filter
        auxscore_card = handle_auxscore_filter(quantity, counter.usrbin_counter, 'USRBIN')
        if auxscore_card:
            output.append(auxscore_card)

    return '\n'.join([f'{card!s}' for card in output])


def handle_auxscore_filter(quantity: Quantity, score_index: int, score_card_type: str = 'USRBIN') -> str:
    """Creates AUXSCORE card for previously created card"""
    filter_value: Optional[Union[int, str]] = parse_filter_value(quantity.scoring_filter)
    if filter_value is None:
        return ''
    auxscore = Card(codewd='AUXSCORE')
    auxscore.what = [
        score_card_type,
        filter_value,
        '',
        score_index,
        score_index,
        1,
    ]
    auxscore.sdum = ''

    return f'{auxscore!s}'


def parse_filter_value(scoring_filter: Union[CustomFilter, ParticleFilter]) -> Optional[Union[int, str]]:
    """Parses filter value from filter"""
    if isinstance(scoring_filter, ParticleFilter):
        return scoring_filter.particle
    if isinstance(scoring_filter, CustomFilter):
        scoring_filter: CustomFilter
        # According to:
        # https://flukafiles.web.cern.ch/manual/chapters/description_input/description_options/auxscore.html#auxscore
        # We are using -(Z*100 + A*100000) for custom filters to define filter
        # for particles with atomic number equal to Z and mass number equal to A
        return -(scoring_filter.z * 100 + scoring_filter.a * 100000)

    return None


@dataclass
class ScoringsCard:
    """Class representing ScoringCard"""

    data: list[Scoring] = field(default_factory=list)

    def __str__(self) -> str:
        # each Scoring card consists of two cards;
        # the second one is continuation of data included in first

        # temporary default for no symmetry
        result: list[str] = []

        default_output_unit = 21
        counter = ScoringCardIndexCounter()
        for scoring in self.data:
            scoring_cards = handle_scoring_cards(default_output_unit, scoring, counter)
            if scoring_cards:
                result.append(scoring_cards)
            default_output_unit += 1
        return '\n'.join(result).strip()
