from dataclasses import dataclass


@dataclass
class Detector:
    """Class representing Detector"""

    name: str
    x_min: float
    x_max: float
    x_bins: int
    y_min: float
    y_max: float
    y_bins: int
    z_min: float
    z_max: float
    z_bins: int


def parse_detector(detector_dict: dict) -> Detector:
    """Creates detector from dictionary"""
    geometry_data = detector_dict['geometryData']
    parameters = geometry_data['parameters']

    depth = parameters['depth']
    height = parameters['height']
    width = parameters['width']

    x_min = get_min_coord(geometry_data['position'][0], width)
    y_min = get_min_coord(geometry_data['position'][1], height)
    z_min = get_min_coord(geometry_data['position'][2], depth)

    x_max = x_min + width
    y_max = y_min + height
    z_max = z_min + depth

    x_bins = parameters['xSegments']
    y_bins = parameters['ySegments']
    z_bins = parameters['zSegments']

    return Detector(
        name=detector_dict['name'],
        x_min=x_min,
        y_min=y_min,
        z_min=z_min,
        x_max=x_max,
        y_max=y_max,
        z_max=z_max,
        x_bins=x_bins,
        y_bins=y_bins,
        z_bins=z_bins
    )


def get_min_coord(center: float, size: float) -> float:
    """Returns minimal coordinate basing on center and size"""
    return center - size / 2
