import math as m
from dataclasses import dataclass
from enum import Enum, unique
from typing import Optional


@unique
class BeamSourceType(Enum):
    """Beam source type"""

    SIMPLE = "simple"
    FILE = "file"
    
    
@unique
class ModulatorSimulationMethod(int, Enum):
    """Modulator simulation method for beam.dat file"""
    def __new__(cls, value, label):
        # Initialise an instance of the Finger enum class 
        obj = int.__new__(cls, value)
        # Calling print(type(obj)) returns <enum 'Finger'>
        # If we don't set the _value_ in the Enum class, an error will be raised.
        obj._value_ = value
        # Here we add an attribute to the finger class on the fly.
        # One may want to use setattr to be more explicit; note the python docs don't do this
        obj.label = label
        return obj

    MODULUS = (0, "modulus")
    SAMPLING = (1, "sampling")
    
    @classmethod
    def from_str(cls, value: str) -> "ModulatorSimulationMethod":
        """Converts a string to a ModulatorSimulationMethod"""
        for method in cls:
            if method.label == value:
                return method

        raise ValueError(f"{cls.__name__} has no value matching {value}")

@unique 
class ModulatorInterpretationMode(int, Enum):
    """Modulator interpretation mode of data in the input files loaded with the USEBMOD card"""
    def __new__(cls, value, label):
        # Initialise an instance of the Finger enum class 
        obj = int.__new__(cls, value)
        # Calling print(type(obj)) returns <enum 'Finger'>
        # If we don't set the _value_ in the Enum class, an error will be raised.
        obj._value_ = value
        # Here we add an attribute to the finger class on the fly.
        # One may want to use setattr to be more explicit; note the python docs don't do this
        obj.label = label
        return obj
    
    MATERIAL = (0, "material")
    VACUMM = (1, "vacumm")
    
    @classmethod
    def from_str(cls, value: str) -> "ModulatorSimulationMethod":
        """Converts a string to a ModulatorSimulationMethod"""
        for method in cls:
            if method.label == value:
                return method

        raise ValueError(f"{cls.__name__} has no value matching {value}")
    


@unique
class StragglingModel(Enum):
    """Straggle model"""

    GAUSSIAN = "Gaussian"
    VAVILOV = "Vavilov"
    NO_STRAGGLING = "no straggling"

    @staticmethod
    def from_str(value: str) -> "StragglingModel":
        """Documentation needed"""
        for model in StragglingModel:
            if model.value == value:
                return model

        raise ValueError(f"Straggle not recognized:{value}")


@unique
class MultipleScatteringMode(Enum):
    """Multiple scattering mode"""

    GAUSSIAN = "Gaussian"
    MOLIERE = "Moliere"
    NO_SCATTERING = "no scattering"

    @staticmethod
    def from_str(value: str) -> "MultipleScatteringMode":
        """Documentation needed"""
        for model in MultipleScatteringMode:
            if model.value == value:
                return model

        raise ValueError(f"Multiple scattering mode not recognized:{value}")


@dataclass
class BeamConfig:
    """Class mapping of the beam.dat config file."""

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
    
    modulator_source_filename: Optional[str] = None
    modulator_source_file_content: Optional[str] = None
    modulator_zone_id: Optional[int] = None
    modulator_simulation: ModulatorSimulationMethod = ModulatorSimulationMethod.MODULUS
    modulator_mode: ModulatorInterpretationMode = ModulatorInterpretationMode.MATERIAL
    
    straggling: StragglingModel = StragglingModel.VAVILOV
    multiple_scattering: MultipleScatteringMode = MultipleScatteringMode.MOLIERE

    energy_cutoff_template = "TCUT0 {energy_low_cutoff} {energy_high_cutoff}  ! energy cutoffs [MeV]"
    sad_template = "BEAMSAD {sad_x} {sad_y}  ! BEAMSAD value [cm]"
    modulator_template = """USEBMOD         {zone} {filename} ! Zone# and file name for beam modulator
BMODMC          {simulation}            ! Simulation method for beam modulator (0-Modulus, 1-Monte Carlo sampling)
BMODTRANS       {mode}            ! Interpretation of thicknesses data in the config file (0-Material, 1-Vacuum)"""
    beam_source_type: BeamSourceType = BeamSourceType.SIMPLE
    beam_source_filename: Optional[str] = None
    beam_source_file_content: Optional[str] = None

    beam_dat_template: str = """
RNDSEED      	89736501     ! Random seed
JPART0       	2            ! Incident particle type
TMAX0      	{energy} {energy_spread}       ! Incident energy and energy spread; both in (MeV/nucl)
{optional_energy_cut_off_line}
NSTAT       {n_stat:d}    0       ! NSTAT, Step of saving
STRAGG          {straggling}            ! Straggling: 0-Off 1-Gauss, 2-Vavilov
MSCAT           {multiple_scattering}            ! Mult. scatt 0-Off 1-Gauss, 2-Moliere
NUCRE           {nuclear_reactions}            ! Nucl.Reac. switcher: 1-ON, 0-OFF
{optional_beam_modulator_lines}
BEAMPOS {pos_x} {pos_y} {pos_z} ! Position of the beam
BEAMDIR {theta} {phi} ! Direction of the beam
BEAMSIGMA  {beam_ext_x} {beam_ext_y}  ! Beam extension
{optional_sad_parameter_line}
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

    @staticmethod
    def _parse_straggle(value: StragglingModel) -> int:
        """Documentation needed"""
        if value == StragglingModel.GAUSSIAN:
            return 1
        if value == StragglingModel.VAVILOV:
            return 2
        if value == StragglingModel.NO_STRAGGLING:
            return 0

        # return default value if no reasonable value is provided
        return 2

    @staticmethod
    def _parse_multiple_scattering(value: MultipleScatteringMode) -> int:
        """Documentation needed"""
        if value == MultipleScatteringMode.GAUSSIAN:
            return 1
        if value == MultipleScatteringMode.MOLIERE:
            return 2
        if value == MultipleScatteringMode.NO_SCATTERING:
            return 0

        # return default value if no reasonable value is provided
        return 2

    def __str__(self) -> str:
        """Return the beam.dat config file as a string."""
        theta, phi, _ = BeamConfig.cartesian2spherical(self.beam_dir)

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
                sad_y=sad_y_value
            )
            
        # if beam modulator was defined, add it to the template
        mod_lines = "! no beam modulator"
        if self.modulator_source_filename is not None and self.modulator_source_file_content is not None and self.modulator_zone_id is not None:
            # if modulator_zone_id is tuple, convert it to int
            if isinstance(self.modulator_zone_id, tuple):
                self.modulator_zone_id = int(self.modulator_zone_id[0])
            mod_lines = BeamConfig.modulator_template.format(
                zone=self.modulator_zone_id, 
                filename=self.modulator_source_filename, 
                simulation=self.modulator_simulation, 
                mode=self.modulator_mode
            )

        # prepare main template
        result = self.beam_dat_template.format(
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
            straggling=self._parse_straggle(self.straggling),
            multiple_scattering=self._parse_multiple_scattering(self.multiple_scattering)
        )

        # if beam source type is file, add the file name to the template
        if self.beam_source_type == BeamSourceType.FILE:
            result += "USECBEAM   sobp.dat   ! Use custom beam source file"

        return result
