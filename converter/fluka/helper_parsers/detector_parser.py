from dataclasses import dataclass


@dataclass
class MeshDetector:
    """Class representing detector with cartesian mesh coordinates"""

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

    @classmethod
    def parse_mesh_detector(cls, detector_dict: dict) -> 'MeshDetector':
        """Creates detector from dictionary"""
        geometry_data = detector_dict['geometryData']
        parameters = geometry_data['parameters']

        depth = parameters['depth']
        height = parameters['height']
        width = parameters['width']

        x_min = cls.__get_min_coord(geometry_data['position'][0], width)
        y_min = cls.__get_min_coord(geometry_data['position'][1], height)
        z_min = cls.__get_min_coord(geometry_data['position'][2], depth)

        x_max = x_min + width
        y_max = y_min + height
        z_max = z_min + depth

        x_bins = parameters['xSegments']
        y_bins = parameters['ySegments']
        z_bins = parameters['zSegments']

        return MeshDetector(name=detector_dict['name'],
                            x_min=x_min,
                            y_min=y_min,
                            z_min=z_min,
                            x_max=x_max,
                            y_max=y_max,
                            z_max=z_max,
                            x_bins=x_bins,
                            y_bins=y_bins,
                            z_bins=z_bins)

    def __get_min_coord(center: float, size: float) -> float:
        """Returns minimal coordinate basing on center and size"""
        return center - size / 2


@dataclass
class CylinderDetector:
    """Class representing detector with in shape of cylinder"""

    name: str
    x: float
    y: float
    r_min: float
    r_max: float
    z_min: float
    z_max: float
    r_bins: int
    z_bins: int
    phi_bins: int

    @classmethod
    def parse_cylinder_detector(cls, detector_dict: dict) -> 'CylinderDetector':
        """Creates detector from dictionary"""
        geometry_data = detector_dict['geometryData']
        parameters = geometry_data['parameters']

        x = geometry_data['position'][0]
        y = geometry_data['position'][1]

        r_min = parameters['innerRadius']
        r_max = parameters['radius']

        depth = parameters['depth']
        z_min = cls.__get_min_coord(geometry_data['position'][2], depth)
        z_max = z_min + depth

        r_bins = parameters['radialSegments']
        z_bins = parameters['zSegments']

        # default from fluka documentation, not provided in json dict
        phi_bins = 1

        return CylinderDetector(name=detector_dict['name'],
                                x=x,
                                y=y,
                                r_min=r_min,
                                r_max=r_max,
                                z_min=z_min,
                                z_max=z_max,
                                r_bins=r_bins,
                                z_bins=z_bins,
                                phi_bins=phi_bins
        )

    def __get_min_coord(center: float, size: float) -> float:
        """Returns minimal coordinate basing on center and size"""
        return center - size / 2
