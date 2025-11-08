from pathlib import Path
from math import log10, ceil, isclose, sin, cos, radians

class Parser:
    """Abstract parser, the template for implementing other parsers."""

    def __init__(self) -> None:
        self.info = {
            'version': '',
            'label': '',
            'simulator': '',
        }

    def parse_configs(self, json: dict) -> None:
        """Convert the json dict to the 4 config dataclasses."""
        raise NotImplementedError

    def save_configs(self, target_dir: str):
        """
        Save the configs as text files in the target_dir.
        The files are: beam.dat, mat.dat, detect.dat and geo.dat.
        """
        if not Path(target_dir).exists():
            raise ValueError('Target directory does not exist.')

        for file_name, content in self.get_configs_json().items():
            with open(Path(target_dir, file_name), 'w') as conf_f:
                conf_f.write(content)

    def get_configs_json(self) -> dict:
        """
        Return a dict representation of the config files. Each element has
        the config files name as key and its content as value.
        """
        configs_json = {
            'info.json': str(self.info),
        }
        return configs_json


def format_float(number: float, n: int) -> float:
    """
    Format float to be up to n characters wide, as precise as possible and as short
    as possible (in descending priority). so for example given 12.333 for n=5 you will
    get 12.33, n=7 will be 12.333
    """
    result = number
    # If number is zero we just want to get 0.0 (it would mess up the log10 operation below)
    if isclose(result, 0., rel_tol=1e-9):
        return 0.

    length = n

    # Adjust length for decimal separator ('.')
    length -= 1

    # Sign messes up the log10 we use do determine how long the number is. We use
    # abs() to fix that, but we need to remember the sign and update `n` accordingly
    sign = 1

    if number < 0:
        result = abs(number)
        sign = -1
        # Adjust length for the sign
        length -= 1

    whole_length = ceil(log10(result))

    # Check if it will be possible to fit the number
    if whole_length > length - 1:
        raise ValueError(f'Number is to big to be formatted. Minimum length: {whole_length-sign+1},\
requested length: {n}')

    # Adjust n for the whole numbers, log returns reasonable outputs for values greater
    # than 1, for other values it returns nonpositive numbers, but we would like 1
    # to be returned. We solve that by taking the greater value between the returned and
    # and 1.
    length -= max(whole_length, 1)

    result = float(sign * round(result, length))

    # Check if the round function truncated the number, warn the user if it did.
    if not isclose(result, number):
        print(f'WARN: number was truncated when converting: {number} -> {result}')

    # Formatting negative numbers smaller than the desired precision could result in -0.0 or 0.0 randomly.
    # To avoid this we catch -0.0 and return 0.0.
    if isclose(result, 0., rel_tol=1e-9):
        return 0.

    return result


def convert_beam_energy(particles_dict, particle_id, a, energy, energy_unit):
    """
    Validates that energy_unit is listed `particles_dict.available_units`
    and converts it to `particles_dict.target_unit` if necessary.

    :returns: tuple `(energy, energy unit, scale factor)` after conversion
    """
    particle_parser_metadata = particles_dict[particle_id]
    allowed_units = particle_parser_metadata["allowed_units"]
    energy_unit = energy_unit

    # Check if unit is allowed (i.e. MeV/nucl doesn't make sense for kaons, muons, etc.)
    if energy_unit not in allowed_units:
        particle_name = particle_parser_metadata["name"]
        raise ValueError(f"Unit '{energy_unit}' not allowed for particle '{particle_name}'")

    # Convert to target unit and save the converted unit for display
    if particle_parser_metadata['target_unit'] == 'MeV/nucl' and energy_unit == 'MeV':
        # converting from MeV to MeV/nucl means we need to divide kinetic energy by mass number A
        energy_scale_factor = 1 / a
        energy_unit = particle_parser_metadata['target_unit']
    elif particle_parser_metadata['target_unit'] == 'MeV' and energy_unit == 'MeV/nucl':
        energy_scale_factor = a
        energy_unit = particle_parser_metadata['target_unit']
    else:
        # everything is correct
        energy_scale_factor = 1

    return energy * energy_scale_factor, energy_unit, energy_scale_factor


def rotate(vector: list[float], angles: list[float], degrees: bool = True) -> list[float]:
    """
    Rotate a vector in 3D around XYZ axes, assuming Euler angles.

    Proper Euler angles uses z-x-z, x-y-x, y-z-y, z-y-z, x-z-x, y-x-y axis sequences, here we
    stick to other convention called Tait-Bryan angles. First we rotate vector around X axis by first
    angle, then around Y axis and finally around Z axis, The individual rotations are
    usually known as yaw, pitch and roll.

    If degrees is True, then the given angle are assumed to be in degrees. Otherwise radians are used.
    """
    # Convert angles to radians if degrees is True

    rad_angles = [radians(angle) for angle in angles] if degrees else angles

    x, y, z = vector
    new_x, new_y, new_z = 0, 0, 0

    # Rotation around x-axis
    new_x = x
    new_y = y * cos(rad_angles[0]) - z * sin(rad_angles[0])
    new_z = y * sin(rad_angles[0]) + z * cos(rad_angles[0])

    # Rotation around y-axis
    new_x2 = new_x * cos(rad_angles[1]) + new_z * sin(rad_angles[1])
    new_y2 = new_y
    new_z2 = -new_x * sin(rad_angles[1]) + new_z * cos(rad_angles[1])

    # Rotation around z-axis
    new_x3 = new_x2 * cos(rad_angles[2]) - new_y2 * sin(rad_angles[2])
    new_y3 = new_x2 * sin(rad_angles[2]) + new_y2 * cos(rad_angles[2])
    new_z3 = new_z2

    return [new_x3, new_y3, new_z3]
