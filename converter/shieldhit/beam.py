import math as m
from dataclasses import dataclass
from enum import IntEnum, unique
from typing import Optional, TypeVar, Type


T = TypeVar("T", bound="LabelledEnum")


class LabelledEnum(IntEnum):
    """Base class for enums with a label attribute"""

    label: str

    def __new__(cls, value, label):

        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        return obj

    @classmethod
    def from_str(cls: Type[T], value: str) -> T:
        """Converts a string to a LabelledEnum"""
        for method in cls:
            if method.label == value:
                return method

        raise ValueError(f"{cls.__name__} has no value matching {value}")


@unique
class BeamSourceType(LabelledEnum):
    """Beam source type"""

    SIMPLE = (0, "simple")
    FILE = (1, "file")


@unique
class ModulatorSimulationMethod(LabelledEnum):
    """Modulator simulation method for beam.dat file"""

    MODULUS = (0, "modulus")
    SAMPLING = (1, "sampling")


@unique
class ModulatorInterpretationMode(LabelledEnum):
    """Modulator interpretation mode of data in the input files loaded with the USEBMOD card"""

    MATERIAL = (0, "material")
    VACUMM = (1, "vacumm")


@unique
class StragglingModel(LabelledEnum):
    """Straggle model"""

    GAUSSIAN = (1, "Gaussian")
    VAVILOV = (2, "Vavilov")
    NO_STRAGGLING = (0, "no straggling")


@unique
class MultipleScatteringMode(LabelledEnum):
    """Multiple scattering mode"""

    GAUSSIAN = (1, "Gaussian")
    MOLIERE = (2, "Moliere")
    NO_SCATTERING = (0, "no scattering")


@dataclass(frozen=True)
class BeamModulator():
    """Beam modulator card dataclass used in BeamConfig."""

    filename: str
    file_content: str
    zone_id: int
    simulation: ModulatorSimulationMethod = ModulatorSimulationMethod.MODULUS
    mode: ModulatorInterpretationMode = ModulatorInterpretationMode.MATERIAL

    def __str__(self) -> str:
        """Returns the string representation of the beam modulator card"""
        modulator_template = """USEBMOD         {zone} {filename} ! Zone# and file name for beam modulator
BMODMC          {simulation}            ! Simulation method for beam modulator (0-Modulus, 1-Monte Carlo sampling)
BMODTRANS       {mode}            ! Interpretation of thicknesses data in the config file (0-Material, 1-Vacuum)"""
        return modulator_template.format(
            zone=self.zone_id,
            filename=self.filename,
            simulation=self.simulation,
            mode=self.mode)


@dataclass
class BeamConfig:
    """Class mapping of the beam.dat config file."""

    particle: int = 2
    particle_name: Optional[str] = None
    heavy_ion_a: int = 1
    heavy_ion_z: int = 1
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

    heavy_ion_template = "HIPROJ       	{a} {z}           ! A and Z of the heavy ion"
    energy_cutoff_template = "TCUT0       {energy_low_cutoff} {energy_high_cutoff}  ! energy cutoffs [MeV]"
    sad_template = "BEAMSAD {sad_x} {sad_y}  ! BEAMSAD value [cm]"
    beam_source_type: BeamSourceType = BeamSourceType.SIMPLE
    beam_source_filename: Optional[str] = None
    beam_source_file_content: Optional[str] = None

    beam_dat_template: str = """
RNDSEED      	89736501     ! Random seed
JPART0       	{particle}            ! Incident particle type{particle_optional_comment}
{optional_heavy_ion_line}
TMAX0      	{energy} {energy_spread}       ! Incident energy and energy spread; both in (MeV/nucl)
{optional_energy_cut_off_line}
NSTAT       {n_stat:d}    0       ! NSTAT, Step of saving
STRAGG          {straggling}            ! Straggling: 0-Off 1-Gauss, 2-Vavilov
MSCAT           {multiple_scattering}            ! Mult. scatt 0-Off 1-Gauss, 2-Moliere
NUCRE           {nuclear_reactions}            ! Nucl.Reac. switcher: 1-ON, 0-OFF
{optional_beam_modulator_lines}
BEAMPOS         {pos_x} {pos_y} {pos_z} ! Position of the beam
BEAMDIR         {theta} {phi} ! Direction of the beam
BEAMSIGMA       {beam_ext_x} {beam_ext_y}  ! Beam extension
{optional_sad_parameter_line}
DELTAE          {delta_e}   ! relative mean energy loss per transportation step
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
        # acos returns the angle in radians between 0 and pi
        theta = m.degrees(m.acos(z / r))
        # atan2 returns the angle in radians between -pi and pi
        phi = m.degrees(m.atan2(y, x))
        # lets ensure the angle in degrees is always between 0 and 360, as SHIELD-HIT12A requires
        if phi < 0.:
            phi += 360.
        return theta, phi, r

    def __str__(self) -> str:
        """Return the beam.dat config file as a string."""
        theta, phi, _ = BeamConfig.cartesian2spherical(self.beam_dir)

        # if particle name is defined, add the comment to the template
        particle_optional_comment = ""
        if self.particle_name:
            particle_optional_comment = f" ({self.particle_name})"

        # if particle is heavy ion, add the heavy ion line to the template
        heavy_ion_line = "! no heavy ion"
        if self.particle == 25:
            heavy_ion_line = BeamConfig.heavy_ion_template.format(a=self.heavy_ion_a, z=self.heavy_ion_z)

        # if energy cutoffs are defined, add them to the template
        cutoff_line = "! no energy cutoffs"
        if self.energy_low_cutoff is not None and self.energy_high_cutoff is not None:
            cutoff_line = BeamConfig.energy_cutoff_template.format(
                energy_low_cutoff=self.energy_low_cutoff,
                energy_high_cutoff=self.energy_high_cutoff
            )

        # if sad was defined, add it to the template
        sad_line = "! no BEAMSAD value"
        if self.sad_x is not None or self.sad_y is not None:
            sad_y_value = self.sad_y if self.sad_y is not None else ""
            sad_line = BeamConfig.sad_template.format(
                sad_x=self.sad_x,
                sad_y=sad_y_value)

        # if beam modulator was defined, add it to the template
        mod_lines = str(self.modulator) if self.modulator is not None else '! no beam modulator'

        # prepare main template
        result = self.beam_dat_template.format(
            particle=self.particle,
            particle_optional_comment=particle_optional_comment,
            optional_heavy_ion_line=heavy_ion_line,
            energy=float(self.energy),
            energy_spread=float(self.energy_spread),
            optional_energy_cut_off_line=cutoff_line,
            optional_sad_parameter_line=sad_line,
            optional_beam_modulator_lines=mod_lines,
            n_stat=self.n_stat,
            pos_x=self.beam_pos[0],
            pos_y=self.beam_pos[1],
            pos_z=self.beam_pos[2],
            beam_ext_x=self.beam_ext_x,
            beam_ext_y=self.beam_ext_y,
            theta=theta,
            phi=phi,
            delta_e=self.delta_e,
            nuclear_reactions=1 if self.nuclear_reactions else 0,
            straggling=self.straggling.value,
            multiple_scattering=self.multiple_scattering.value
        )

        # if beam source type is file, add the file name to the template
        if self.beam_source_type == BeamSourceType.FILE:
            result += "USECBEAM   sobp.dat   ! Use custom beam source file"

        return result
