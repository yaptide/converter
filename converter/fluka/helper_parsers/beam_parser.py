from dataclasses import dataclass
from enum import Enum

from converter.common import cartesian2spherical

class BeamShape(Enum):
    """Enum representing beam shape"""

    GAUSSIAN = 1
    SQUARE = 2
    CIRCULAR = 3

class BeamShapeParams:
    shape: BeamShape = BeamShape.GAUSSIAN

class RoundBeamShapeParams(BeamShapeParams):
    radius: float = 0

class SquareBeamShapeParams(BeamShapeParams):
    width: float = 0
    height: float = 0

class GaussianBeamShapeParams(BeamShapeParams):
    sigma_x: float = 0
    sigma_y: float = 0

@dataclass(frozen=False)
class FlukaBeam:
    """Class representing beam config in a FLUKA input file."""
    energy: float = 150.  # [MeV]
    beam_pos: tuple[float, float, float] = (0, 0, 0)  # [cm]
    beam_dir: tuple[float, float, float] = (0, 0)  # [cm]
    shape_params: BeamShapeParams = GaussianBeamShapeParams()
    particle_type: int = 2


def parse_particle(particle_json: dict):
    """Parse particle ID to FLUKA particle name."""
    particle_id = particle_json["id"]
    if particle_id == 1:
        return "NEUTRON"
    elif particle_id == 2:
        return "PROTON"
    elif particle_id == 3:
        return "PION-"
    elif particle_id == 4:
        return "PION+"
    elif particle_id == 5:
        return "PIZERO"
    elif particle_id == 6:
        return "ANEUTRON"
    elif particle_id == 7:
        return "APROTON"
    elif particle_id == 8:
        return "KAON-"
    elif particle_id == 9:
        return "KAON+"
    elif particle_id == 10: # k0 ?
        return "KAONZERO"
    elif particle_id == 11: # k~ ?
        return "KAONLONG"
    elif particle_id == 12: # gamma ?
        return ""
    elif particle_id == 15:
        return "MUON-"
    elif particle_id == 16:
        return "MUON+"
    elif particle_id == 21:
        return "DEUTERON"
    elif particle_id == 22:
        return "TRITON"
    elif particle_id == 23:
        return "3-HELIUM"
    elif particle_id == 24:
        return "4-HELIUM"
    elif particle_id == 25:
        return "HEAVYION"
    else:
        raise ValueError("Particle ID not supported by FLUKA")


def parse_shape_params(shape_params_json: dict) -> BeamShapeParams:
    """Parse shape params from JSON to FLUKA shape params."""
    # TODO
    shape = BeamShape(shape_params_json["type"])
    if shape == BeamShape.GAUSSIAN:
        shape_params = GaussianBeamShapeParams()
        shape_params.sigma_x = shape_params_json["sigmaX"]
        shape_params.sigma_y = shape_params_json["sigmaY"]
    elif shape == BeamShape.SQUARE:
        shape_params = SquareBeamShapeParams()
        shape_params.width = shape_params_json["width"]
        shape_params.height = shape_params_json["height"]
    elif shape == BeamShape.CIRCULAR:
        shape_params = RoundBeamShapeParams()
        shape_params.radius = shape_params_json["radius"]
    else:
        raise ValueError("Beam shape not supported by FLUKA")
    return shape_params


def parse_beam(beam_json: dict) -> FlukaBeam:
    """Parse beam from JSON to FLUKA beam."""
    fluka_beam = FlukaBeam()
    fluka_beam.energy = beam_json["energy"] # convert to gev
    fluka_beam.beam_pos = tuple(beam_json["position"])
    fluka_beam.beam_dir = tuple(beam_json["direction"])
    fluka_beam.particle_type = parse_particle(beam_json["particle"])
    fluka_beam.shape_params = parse_shape_params(beam_json["sigma"])
    theta, phi, _ = cartesian2spherical(fluka_beam.beam_dir) # convert to cosines

    return fluka_beam