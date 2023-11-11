from dataclasses import dataclass, field
from converter.fluka.cards.card import Card
from converter.fluka.helper_parsers.beam_parser import BeamShape, FlukaBeam

@dataclass
class BeamCard:
    """Class representing description of beam in Fluka input"""

    data: FlukaBeam = field(default_factory=lambda: FlukaBeam())

    def __str__(self) -> str:
        """Return the card as a string."""
        beam_card = Card(tag="BEAM")
        if self.data.shape == BeamShape.GAUSSIAN:
            shape_what = -1
            x_y_multiplier = -1
        elif self.data.shape == BeamShape.CIRCULAR:
            shape_what = -1
            x_y_multiplier = 1
        else:
            shape_what = 0
            x_y_multiplier = 1
        beam_card.what = [self.data.energy*-1, 0, 0, self.data.shape_x*x_y_multiplier, self.data.shape_y*x_y_multiplier, shape_what]
        beam_card.sdum = self.data.particle_name
        if self.data.particle_name == "HEAVYION":
            hi_card = Card(tag="HI-PROPE")
            hi_card.what = [self.data.heavy_ion_a, self.data.heavy_ion_z, 0, 0, 0, 0]

        beamposition_card = Card(tag="BEAMPOS")
        if self.data.z_negative:
            z_sdum = "NEGATIVE"
        else:
            z_sdum = ""
        beamposition_card.what = [self.data.beam_pos[0], self.data.beam_pos[1], self.data.beam_pos[2], self.data.beam_dir[0], self.data.beam_dir[1], 0]
        beamposition_card.sdum = z_sdum

        result = beam_card.__str__() + "\n"
        if self.data.particle_name == "HEAVYION":
            result += hi_card.__str__() + "\n"
        result += beamposition_card.__str__()
        # TODO: add comments
        return result