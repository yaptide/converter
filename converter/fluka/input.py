from dataclasses import dataclass


@dataclass
class Input:
    """Class mapping of the fluka input file."""

    energy_GeV: float = 90.0  # GeV FLUKA specific
    number_of_particles: int = 1000

    template: str = """TITLE
proton beam simulation
* default physics settings for hadron therapy
DEFAULTS                                                              HADROTHE
* beam source
BEAM      {energy_GeV:>10.3E}                                                  PROTON
* beam source position
BEAMPOS          0.0       0.0    -100.0
* geometry description starts here
GEOBEGIN                                                              COMBNAME
    0    0
* black body sphere
SPH blkbody    0.0 0.0 0.0 10000.0
* air shpere
SPH air        0.0 0.0 0.0 100.0
* target cylinder
RCC target     0.0 0.0 0.0 0.0 0.0 10.0 5.0
END
* outer black body region
Z_BBODY      5 +blkbody -air
* inner air region
Z_AIR        5 +air -target
* target region
Z_TARGET     5 +target
END
GEOEND
ASSIGNMA    BLCKHOLE   Z_BBODY
ASSIGNMA         AIR     Z_AIR
ASSIGNMA       WATER  Z_TARGET
* scoring NEUTRON on mesh z
USRBIN           0.0   NEUTRON       -21       0.5       0.5       5.0n_z
USRBIN          -0.5      -0.5       0.0         1         1       500&
* scoring NEUTRON on mesh yz
USRBIN           0.0   NEUTRON       -22       0.1       5.0       5.0n_yz
USRBIN          -0.1      -5.0       0.0         1       500       500&
* scoring NEUTRON on mesh xy
USRBIN           0.0   NEUTRON       -23       5.0       5.0       2.9n_xy
USRBIN          -5.0      -5.0       2.8       500       500         1&
* scoring NEUTRON on mesh zx
USRBIN           0.0   NEUTRON       -24       5.0       0.1       5.0n_zx
USRBIN          -5.0      -0.1       0.0       500         1       500&
* scoring ENERGY on mesh z
USRBIN           0.0    ENERGY       -25       0.5       0.5       5.0en_z
USRBIN          -0.5      -0.5       0.0         1         1       500&
* scoring ENERGY on mesh yz
USRBIN           0.0    ENERGY       -26       0.1       5.0       5.0en_yz
USRBIN          -0.1      -5.0       0.0         1       500       500&
* scoring ENERGY on mesh xy
USRBIN           0.0    ENERGY       -27       5.0       5.0       2.9en_xy
USRBIN          -5.0      -5.0       2.8       500       500         1&
* scoring ENERGY on mesh zx
USRBIN           0.0    ENERGY       -28       5.0       0.1       5.0en_zx
USRBIN          -5.0      -0.1       0.0       500         1       500&
* random number generator settings
RANDOMIZ                   137
* number of particles to simulate
START     {number_of_particles:>10}
STOP
"""

    def __str__(self):
        """Return fluka input file as string"""
        return self.template.format(
            energy_GeV=-self.energy_GeV,
            number_of_particles=self.number_of_particles,
        )
