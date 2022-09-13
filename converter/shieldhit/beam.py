from dataclasses import dataclass
import math as m


@dataclass
class BeamConfig:
    """Class mapping of the beam.dat config file."""

    energy: float = 150.
    energy_spread: float = 1.5
    beam_ext_x: float = -0.1
    beam_ext_y: float = 0.1
    delta_e: float = 0.03
    nstat: int = 10000
    beampos: tuple[float, float, float] = (0, 0, 0)
    beamdir: tuple[float, float, float] = (0, 0, 1)

    beam_template: str = """
RNDSEED      	89736501     ! Random seed
JPART0       	2            ! Incident particle type
TMAX0      	{energy}  {energy_spread}       ! Incident energy; (MeV/nucl)
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
        return self.beam_template.format(
            energy=self.energy,
            energy_spread=self.energy_spread,
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
