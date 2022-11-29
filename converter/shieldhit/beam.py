from dataclasses import dataclass
import math as m
from enum import Enum, unique
from typing import Optional

@unique
class BeamSourceType(Enum):
    """Beam source type"""

    SIMPLE = "simple"

    FILE = "file"


@dataclass
class BeamConfig:
    """Class mapping of the beam.dat config file."""

    energy: float = 150.  # [MeV]
    energy_spread: float = 1.5  # [MeV]
    energy_low_cutoff: Optional[float] = None  # [MeV]
    energy_high_cutoff: Optional[float] = None  # [MeV]
    beam_ext_x: float = -0.1  # [cm]
    beam_ext_y: float = 0.1  # [cm]
    nstat: int = 10000
    beampos: tuple[float, float, float] = (0, 0, 0)  # [cm]
    beamdir: tuple[float, float, float] = (0, 0, 1)  # [cm]
    delta_e: float = 0.03  # [a.u.]

    cutoff_template = "TCUT0 {energy_low_cutoff} {energy_high_cutoff}  ! energy cutoffs [MeV]"
    definition_type: BeamSourceType = BeamSourceType.SIMPLE
    definition_file: Optional[str] = None

    beam_template: str = """
RNDSEED      	89736501     ! Random seed
JPART0       	2            ! Incident particle type
TMAX0      	{energy} {energy_spread}       ! Incident energy and energy spread; both in (MeV/nucl)
{optional_energy_cut_off_line}
NSTAT       {nstat:d}    0       ! NSTAT, Step of saving
STRAGG          2            ! Straggling: 0-Off 1-Gauss, 2-Vavilov
MSCAT           2            ! Mult. scatt 0-Off 1-Gauss, 2-Moliere
NUCRE           1            ! Nucl.Reac. switcher: 1-ON, 0-OFF
BEAMPOS {pos_x} {pos_y} {pos_z} ! Position of the beam
BEAMDIR {theta} {phi} ! Direction of the beam
BEAMSIGMA  {beam_ext_x} {beam_ext_y}  ! Beam extension
DELTAE   {delta_e}   ! relative mean energy loss per transportation step
"""

    @staticmethod
    def cartesian2spherical(vector: tuple[float, float, float]) -> tuple[float, float, float]:
        """
        Transform cartesian coordinates to spherical coordinates.

        :param vector: cartesian coordinates
        :return: spherical coordinates
        """
        x, y, z = vector
        r = m.sqrt(x**2 + y**2 + z**2)
        theta = m.degrees(m.acos(z / r))  # acos returns the angle in radians between 0 and pi
        phi = m.degrees(m.atan2(y, x))  # atan2 returns the angle in radians between -pi and pi
        # lets ensure the angle in degrees is always between 0 and 360, as SHIELD-HIT12A requires
        if phi < 0.:
            phi += 360.
        return theta, phi, r

    def __str__(self) -> str:

        theta, phi, _ = BeamConfig.cartesian2spherical(self.beamdir)
        cutoff_line = "! no energy cutoffs"
        if self.energy_low_cutoff is not None and self.energy_high_cutoff is not None:
            cutoff_line = BeamConfig.cutoff_template.format(
                energy_low_cutoff=self.energy_low_cutoff,
                energy_high_cutoff=self.energy_high_cutoff
            )
        result = self.beam_template.format(
            energy=float(self.energy),
            energy_spread=float(self.energy_spread),
            optional_energy_cut_off_line=cutoff_line,
            nstat=self.nstat,
            pos_x=self.beampos[0],
            pos_y=self.beampos[1],
            pos_z=self.beampos[2],
            beam_ext_x=self.beam_ext_x,
            beam_ext_y=self.beam_ext_y,
            theta=theta,
            phi=phi,
            delta_e=self.delta_e
        )

        if self.definition_type == BeamSourceType.FILE:
            result += "USECBEAM   sobp.dat   ! Use custom beam source file"

        return result
