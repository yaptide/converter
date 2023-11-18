from math import cos, radians
from dataclasses import dataclass
from enum import Enum

from converter.common import cartesian2spherical


class BeamShape(Enum):
    """Enum representing beam shape"""

    GAUSSIAN = 1
    SQUARE = 2
    CIRCULAR = 3

    def __str__(self):
        if self == BeamShape.GAUSSIAN:
            return "gaussian"
        if self == BeamShape.SQUARE:
            return "flat square"
        if self == BeamShape.CIRCULAR:
            return "flat circular"
        return ""


@dataclass(frozen=False)
class FlukaBeam:
    """Class representing beam config in a FLUKA input file."""

    energy: float = 150.  # [GeV]
    beam_pos: tuple[float, float, float] = (0, 0, 0)  # [cm]
    beam_dir: tuple[float, float] = (0, 0)  # cosines respective to x and y axes
    z_negative: bool = False
    shape: BeamShape = BeamShape.GAUSSIAN
    shape_x: float = 0
    shape_y: float = 0
    particle_name: str = "PROTON"
    heavy_ion_a: int = 1
    heavy_ion_z: int = 1


particle_dict = {
    1: {"name": "NEUTRON", "a": 1},
    2: {"name": "PROTON", "a": 1},
    3: {"name": "PION-", "a": 1},
    4: {"name": "PION+", "a": 1},
    5: {"name": "PIZERO", "a": 1},
    6: {"name": "ANEUTRON", "a": 1},
    7: {"name": "APROTON", "a": 1},
    8: {"name": "KAON-", "a": 1},
    9: {"name": "KAON+", "a": 1},
    10: {"name": "KAONZERO", "a": 1},
    11: {"name": "KAONLONG", "a": 1},
    12: {"name": "PHOTON", "a": 1},
    15: {"name": "MUON-", "a": 1},
    16: {"name": "MUON+", "a": 1},
    21: {"name": "DEUTERON", "a": 2},
    22: {"name": "TRITON", "a": 3},
    23: {"name": "3-HELIUM", "a": 3},
    24: {"name": "4-HELIUM", "a": 4},
    25: {"name": "HEAVYION", "a": 1}
}


def convert_energy_to_gev(beam_json: dict) -> float:
    """Convert energy from MeV/nucl to GeV."""
    energy = beam_json["energy"] / 1000  # convert to GeV
    particle = particle_dict[beam_json["particle"]["id"]]
    if particle["name"] == "HEAVYION":
        return energy * beam_json["particle"]["a"]
    return energy * particle["a"]


def parse_particle_name(particle_json: dict):
    """Parse particle ID to FLUKA particle name."""
    particle_id = particle_json["id"]
    if particle_id in particle_dict:
        particle = particle_dict[particle_id]
        return particle["name"]
    raise ValueError("Particle ID not supported by FLUKA")


def parse_shape_params(shape_params_json: dict) -> tuple[BeamShape, float, float]:
    """Parse shape params from JSON to FLUKA shape params."""
    shape = shape_params_json["type"]
    if shape == "Flat circular":
        return BeamShape.CIRCULAR, shape_params_json["x"], shape_params_json["y"]
    if shape == "Flat square":
        return BeamShape.SQUARE, shape_params_json["x"], shape_params_json["y"]
    if shape == "Gaussian":
        return BeamShape.GAUSSIAN, shape_params_json["x"], shape_params_json["y"]
    raise ValueError("Shape type not supported by FLUKA")


def parse_beam(beam_json: dict) -> FlukaBeam:
    """Parse beam from JSON to FLUKA beam."""
    fluka_beam = FlukaBeam()
    fluka_beam.energy = convert_energy_to_gev(beam_json)
    fluka_beam.particle_name = parse_particle_name(beam_json["particle"])
    if fluka_beam.particle_name == "HEAVYION":
        fluka_beam.heavy_ion_a = beam_json["particle"]["a"]
        fluka_beam.heavy_ion_z = beam_json["particle"]["z"]
    fluka_beam.beam_pos = tuple(beam_json["position"])
    shape, shape_x, shape_y = parse_shape_params(beam_json["sigma"])
    fluka_beam.shape = shape
    fluka_beam.shape_x = shape_x
    fluka_beam.shape_y = shape_y
    theta, phi, _ = cartesian2spherical(beam_json["direction"])
    # FLUKA uses angles respective to x and y axes
    # for example beam going along the z axis has theta = 90, phi = 90
    theta += 90
    phi += 90
    fluka_beam.beam_dir = (cos(radians(theta)), cos(radians(phi)))
    if beam_json["direction"][2] < 0:
        fluka_beam.z_negative = True
    return fluka_beam
