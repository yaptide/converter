from typing import Optional


class FlukaBeam:
    """Class representing beam config in a FLUKA input file."""
    energy: float = 150.  # [MeV]
    energy_spread: float = 1.5  # [MeV]
    energy_low_cutoff: Optional[float] = None  # [MeV]
    energy_high_cutoff: Optional[float] = None  # [MeV]
    beam_ext_x: float = -0.1  # [cm]
    beam_ext_y: float = 0.1  # [cm]
    sad_x: Optional[float] = None  # [cm]
    sad_y: Optional[float] = None  # [cm]
    n_stat: int = 10000
    beam_pos: tuple[float, float, float] = (0, 0, 0)  # [cm]
    beam_dir: tuple[float, float, float] = (0, 0, 1)  # [cm]
    delta_e: float = 0.03  # [a.u.]
    nuclear_reactions: bool = True

    modulator: Optional[BeamModulator] = None

    straggling: StragglingModel = StragglingModel.VAVILOV
    multiple_scattering: MultipleScatteringMode = MultipleScatteringMode.MOLIERE

    energy_cutoff_template = "TCUT0       {energy_low_cutoff} {energy_high_cutoff}  ! energy cutoffs [MeV]"
    sad_template = "BEAMSAD {sad_x} {sad_y}  ! BEAMSAD value [cm]"
    beam_source_type: BeamSourceType = BeamSourceType.SIMPLE