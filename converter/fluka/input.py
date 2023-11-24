from dataclasses import dataclass, field
from converter.fluka.cards.card import Card
from converter.fluka.cards.figure_card import FiguresCard
from converter.fluka.cards.region_card import RegionsCard
from converter.fluka.cards.material_card import MaterialsCard
from converter.fluka.cards.compound_card import CompoundsCard
from converter.fluka.cards.assignmat_card import AssignmatsCard
from converter.fluka.cards.matprop_card import MatpropsCard
from converter.solid_figures import SolidFigure


@dataclass
class Input:
    """Class mapping of the Fluka input file."""

    energy_GeV: float = 0.07  # GeV FLUKA specific
    number_of_particles: int = 10000

    materials: list = field(default_factory=list)
    compounds: list = field(default_factory=list)
    figures: list[SolidFigure] = field(default_factory=list)
    regions: list = field(default_factory=list)
    assignmats: list = field(default_factory=list)
    matprops: list = field(default_factory=list)

    template: str = """TITLE
proton beam simulation
* default physics settings for hadron therapy
DEFAULTS                                                              HADROTHE
* beam source
{BEAM}
* beam source position
BEAMPOS          0.0       0.0    -100.0
* geometry description starts here
GEOBEGIN                                                              COMBNAME
    0    0
{FIGURES}
END
{REGIONS}
END
GEOEND
{MATERIALS}
{COMPOUNDS}
{ASSIGNMATS}
{MATPROPS}
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
{START}
STOP
"""

    def __str__(self):
        """Return fluka input file as string"""
        return self.template.format(
            BEAM=Card(codewd="BEAM", what=[str(-self.energy_GeV)], sdum="PROTON"),
            START=Card(codewd="START", what=[str(self.number_of_particles)]),
            FIGURES=FiguresCard(data=self.figures),
            REGIONS=RegionsCard(data=self.regions),
            MATERIALS=MaterialsCard(data=self.materials),
            COMPOUNDS=CompoundsCard(data=self.compounds),
            ASSIGNMATS=AssignmatsCard(data=self.assignmats),
            MATPROPS=MatpropsCard(data=self.matprops),
        )
