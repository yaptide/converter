from dataclasses import dataclass, field
from converter.common import format_float
from converter.fluka.cards.card import Card
from converter.fluka.helper_parsers.beam_parser import BeamShape, FlukaBeam


@dataclass
class BeamCard:
    """Class representing description of beam in Fluka input"""

    data: FlukaBeam = field(default_factory=lambda: FlukaBeam())  # skipcq: PYL-W0108

    def __str__(self) -> str:
        """Return the card as a string."""
        beam_card = Card(codewd="BEAM")
        if self.data.shape == BeamShape.GAUSSIAN:
            shape_what = -1
            x_y_multiplier = -1
        elif self.data.shape == BeamShape.CIRCULAR:
            shape_what = -1
            x_y_multiplier = 1
        else:
            shape_what = 0
            x_y_multiplier = 1
        # in Fluka input file positive number is interpreted as momentum
        # and negative as energy
        # we store energy in FlukaBeam object as positive number,
        # so we need to multiply it by -1
        # we also divide it by 1000 to convert from MeV to GeV
        momentum_or_energy = format_float(-self.data.energy_MeV / 1000, 10)
        shape_x = format_float(self.data.shape_x*x_y_multiplier, 10)
        shape_y = format_float(self.data.shape_y*x_y_multiplier, 10)
        if self.data.shape == BeamShape.CIRCULAR:
            # swap x and y if beam is circular
            # as circular beam is defined maximum and minimum radius in that order
            # and in radius is provided in y
            shape_x, shape_y = shape_y, shape_x

        beam_card.what = [momentum_or_energy, 0, 0,
                          shape_x, shape_y, shape_what]
        beam_card.sdum = self.data.particle_name
        if self.data.particle_name == "HEAVYION":
            hi_card = Card(codewd="HI-PROPE")
            hi_card.what = [self.data.heavy_ion_z, self.data.heavy_ion_a, 0, 0, 0, 0]

        beamposition_card = Card(codewd="BEAMPOS")

        # z_negative is True if beam direction is negative in respect to z axis
        if self.data.z_negative:
            z_sdum = "NEGATIVE"
        else:
            z_sdum = ""

        pos_x = format_float(self.data.beam_pos[0], 10)
        pos_y = format_float(self.data.beam_pos[1], 10)
        pos_z = format_float(self.data.beam_pos[2], 10)
        dir_x = format_float(self.data.beam_dir[0], 10)
        dir_y = format_float(self.data.beam_dir[1], 10)
        beamposition_card.what = [pos_x, pos_y, pos_z,
                                  dir_x, dir_y, 0]
        beamposition_card.sdum = z_sdum

        result = f"* {self.data.particle_name} beam of energy {-momentum_or_energy} GeV\n"
        if self.data.shape == BeamShape.CIRCULAR:
            result += f"* {self.data.shape} shape with max radius={shape_x} cm, min radius={shape_y} cm\n"
        else:
            result += f"* {self.data.shape} shape with x={shape_x} cm, y={shape_y} cm\n"
        result += beam_card.__str__() + "\n"
        if self.data.particle_name == "HEAVYION":
            result += f"* heavy ion properties: a={self.data.heavy_ion_a}, z={self.data.heavy_ion_z}\n"
            result += hi_card.__str__() + "\n"
        result += (f"* beam position: ({pos_x}, {pos_y}, {pos_z}) cm\n"
                   f"* beam direction cosines in respect to x: {dir_x}, y: {dir_y}\n")
        if self.data.z_negative:
            result += "* beam direction is negative in respect to z axis\n"
        else:
            result += "* beam direction is positive in respect to z axis\n"
        result += beamposition_card.__str__()
        return result