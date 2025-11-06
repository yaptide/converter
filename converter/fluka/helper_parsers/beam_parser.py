from math import cos, atan, pi
from dataclasses import dataclass
from enum import Enum


class BeamShape(Enum):
    """Enum representing beam shape"""

    GAUSSIAN = 1
    SQUARE = 2
    CIRCULAR = 3

    def __str__(self):
        if self == BeamShape.GAUSSIAN:
            return 'gaussian'
        if self == BeamShape.SQUARE:
            return 'flat square'
        if self == BeamShape.CIRCULAR:
            return 'flat circular'
        return ''


@dataclass(frozen=False)
class FlukaBeam:
    """Class representing beam config in a FLUKA input file."""

    energy_MeV: float = 150.
    beam_pos: tuple[float, float, float] = (0, 0, 0)  # [cm]
    beam_dir: tuple[float, float] = (0, 0)  # cosines respective to x and y axes
    z_negative: bool = False
    shape: BeamShape = BeamShape.GAUSSIAN
    shape_x: float = 0
    shape_y: float = 0
    particle_name: str = 'PROTON'
    heavy_ion_a: int = 1
    heavy_ion_z: int = 1


particle_dict = {
    1: {
        'name': 'NEUTRON',
        'a': 1
    },
    2: {
        'name': 'PROTON',
        'a': 1
    },
    3: {
        'name': 'PION-',
        'a': 1
    },
    4: {
        'name': 'PION+',
        'a': 1
    },
    5: {
        'name': 'PIZERO',
        'a': 1
    },
    6: {
        'name': 'ANEUTRON',
        'a': 1
    },
    7: {
        'name': 'APROTON',
        'a': 1
    },
    8: {
        'name': 'KAON-',
        'a': 1
    },
    9: {
        'name': 'KAON+',
        'a': 1
    },
    10: {
        'name': 'KAONZERO',
        'a': 1
    },
    11: {
        'name': 'KAONLONG',
        'a': 1
    },
    12: {
        'name': 'PHOTON',
        'a': 1
    },
    15: {
        'name': 'MUON-',
        'a': 1
    },
    16: {
        'name': 'MUON+',
        'a': 1
    },
    21: {
        'name': 'DEUTERON',
        'a': 2
    },
    22: {
        'name': 'TRITON',
        'a': 3
    },
    23: {
        'name': '3-HELIUM',
        'a': 3
    },
    24: {
        'name': '4-HELIUM',
        'a': 4
    },
    25: {
        'name': 'HEAVYION',
        'a': 1
    },
    26: {
        'name': 'ELECTRON',
        'a': 1
    }
}


def convert_energy(beam_json: dict) -> float:
    """
    Extract energy from beam JSON and provide it in Fluka convention.
    HEAVYION is a special case which requires that energy to be in MeV/u
    (MeV/nucl is taken as an approximation).
    """
    particle = particle_dict[beam_json['particle']['id']]
    energy_unit = beam_json['energyUnit']
    energy = beam_json['energy']

    if particle['name'] == 'HEAVYION':
        return energy if energy_unit == 'MeV/nucl' else energy / beam_json['particle'].get('a', 1)

    return energy if energy_unit == 'MeV' else energy * beam_json['particle'].get('a', 1)


def parse_particle_name(particle_json: dict):
    """Parse particle ID to FLUKA particle name."""
    particle_id = particle_json['id']
    if particle_id in particle_dict:
        particle = particle_dict[particle_id]
        return particle['name']
    raise ValueError('Particle ID not supported by FLUKA')


def parse_shape_params(shape_params_json: dict) -> tuple[BeamShape, float, float]:
    """Parse shape params from JSON to FLUKA shape params."""
    shape = shape_params_json['type']
    if shape == 'Flat circular':
        return BeamShape.CIRCULAR, shape_params_json['x'], shape_params_json['y']
    if shape == 'Flat square':
        return BeamShape.SQUARE, shape_params_json['x'], shape_params_json['y']
    if shape == 'Gaussian':
        return BeamShape.GAUSSIAN, shape_params_json['x'], shape_params_json['y']
    raise ValueError('Shape type not supported by FLUKA')


def cartesian_to_spherical(coords: tuple[float, float, float]):
    """
    Convert cartesian coordinates to spherical coordinates
    and return cosines of angles respective to x and y axes
    """
    x, y, z = coords
    theta = pi / 2
    if x != 0:
        theta = atan(z / x)
    phi = pi / 2
    if y != 0:
        phi = atan((x**2 + z**2)**0.5 / y)
    return cos(theta), cos(phi)


def parse_beam(beam_json: dict) -> FlukaBeam:
    """Parse beam from JSON to FLUKA beam."""
    fluka_beam = FlukaBeam()
    fluka_beam.energy_MeV = convert_energy(beam_json)
    fluka_beam.particle_name = parse_particle_name(beam_json['particle'])
    if fluka_beam.particle_name == 'HEAVYION':
        fluka_beam.heavy_ion_a = beam_json['particle']['a']
        fluka_beam.heavy_ion_z = beam_json['particle']['z']
    fluka_beam.beam_pos = tuple(beam_json['position'])
    shape, shape_x, shape_y = parse_shape_params(beam_json['sigma'])
    fluka_beam.shape = shape
    fluka_beam.shape_x = shape_x
    fluka_beam.shape_y = shape_y
    theta, phi = cartesian_to_spherical(beam_json['direction'])
    fluka_beam.beam_dir = (theta, phi)
    if beam_json['direction'][2] < 0:
        fluka_beam.z_negative = True
    return fluka_beam
