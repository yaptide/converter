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
    x_min, y_min, z_min = geometry_data['position']
    parameters = geometry_data['parameters']

    x_max = x_min + parameters['depth']
    y_max = y_min + parameters['height']
    z_max = z_min + parameters['width']

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
