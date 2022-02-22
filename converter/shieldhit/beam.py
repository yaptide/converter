from dataclasses import dataclass
import math as m


@dataclass
class BeamConfig:
    """Class mapping of the beam.dat config file."""

    energy: float = 150.
    nstat: int = 10000
    beampos: tuple[float, float, float] = (0, 0, 0)
    beamdir: tuple[float, float, float] = (0, 0, 1)

    beam_template: str = """
RNDSEED      	89736501     ! Random seed
JPART0       	2            ! Incident particle type
TMAX0      	{energy:3.1f}  1.5       ! Incident energy; (MeV/nucl)
NSTAT       {nstat:d}    0       ! NSTAT, Step of saving
STRAGG          2            ! Straggling: 0-Off 1-Gauss, 2-Vavilov
MSCAT           2            ! Mult. scatt 0-Off 1-Gauss, 2-Moliere
NUCRE           1            ! Nucl.Reac. switcher: 1-ON, 0-OFF
BEAMPOS {pos_x} {pos_y} {pos_z} ! Position of the beam
BEAMDIR {theta} {phi} ! Direction of the beam
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
        theta = m.degrees(m.acos(z / r))
        phi = m.degrees(m.atan2(y, x))
        return theta, phi, r

    def __str__(self) -> str:

        theta, phi, _ = BeamConfig.cartesian2spherical(self.beamdir)
        return self.beam_template.format(
            energy=self.energy,
            nstat=self.nstat,
            pos_x=self.beampos[0],
            pos_y=self.beampos[1],
            pos_z=self.beampos[2],
            theta=theta,
            phi=phi,
        )
