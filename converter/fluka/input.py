from dataclasses import dataclass, field
from converter.fluka.cards.beam_card import BeamCard
from converter.fluka.cards.card import Card
from converter.fluka.cards.figure_card import FiguresCard
from converter.fluka.cards.region_card import RegionsCard
from converter.fluka.cards.material_card import MaterialsCard
from converter.fluka.cards.compound_card import CompoundsCard
from converter.fluka.cards.assignmat_card import AssignmatsCard
from converter.fluka.cards.matprop_card import MatPropsCard
from converter.fluka.cards.lowmat_card import LowMatsCard
from converter.fluka.helper_parsers.beam_parser import FlukaBeam
from converter.fluka.cards.scoring_card import ScoringsCard
from converter.solid_figures import SolidFigure


@dataclass
class Input:
    """Class mapping of the Fluka input file."""

    beam: FlukaBeam = field(default_factory=lambda: FlukaBeam())  # skipcq: PYL-W0108
    number_of_particles: int = 10000

    materials: list = field(default_factory=list)
    compounds: list = field(default_factory=list)
    figures: list[SolidFigure] = field(default_factory=list)
    regions: list = field(default_factory=list)
    scorings: list = field(default_factory=list)
    assignmats: list = field(default_factory=list)
    matprops: list = field(default_factory=list)
    lowmats: list = field(default_factory=list)

    template: str = """TITLE
proton beam simulation
* default physics settings for hadron therapy
DEFAULTS                                                              HADROTHE
{BEAM}
* geometry description starts here
GEOBEGIN                                                              COMBNAME
    0    0
{FIGURES}
END
{REGIONS}
END
GEOEND
{MATERIALS}
{LOWMATS}
{COMPOUNDS}
{MATPROPS}
{ASSIGNMATS}
* generated scoring cards
{SCORINGS}
* random number generator settings
RANDOMIZ                   137
* number of particles to simulate
{START}
STOP
"""

    def __str__(self):
        """Return fluka input file as string"""
        return self.template.format(
            START=Card(codewd='START', what=[str(self.number_of_particles)]),
            BEAM=BeamCard(data=self.beam),
            FIGURES=FiguresCard(data=self.figures),
            REGIONS=RegionsCard(data=self.regions),
            SCORINGS=ScoringsCard(data=self.scorings),
            MATERIALS=MaterialsCard(data=self.materials),
            LOWMATS=LowMatsCard(data=self.lowmats),
            COMPOUNDS=CompoundsCard(data=self.compounds),
            ASSIGNMATS=AssignmatsCard(data=self.assignmats),
            MATPROPS=MatPropsCard(data=self.matprops),
        )
