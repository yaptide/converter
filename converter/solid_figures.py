from dataclasses import dataclass
from abc import ABC


@dataclass(frozen=True)
class SolidFigure(ABC):
    """
    Abstract solid figure in 3D space. It is characterised by position in
    space and rotation along X,Y,Z axis in its own reference frame. Size of
    the figure (its extend in space) is defined in its subclasses.
    """

    uuid: str
    position: tuple[float, float, float]
    rotation: tuple[float, float, float]


@dataclass(frozen=True)
class SphereFigure(SolidFigure):
    """A sphere. Its size is defined by its radius."""

    radius: float


@dataclass(frozen=True)
class CylinderFigure(SolidFigure):
    """
    A cylinder, a cone or a truncated cone. It's defined by the radii of both of
    its bases(top and bottom) and height. A cone can be created by setting one
    of the radii to zero.
    """

    radius_top: float
    radius_bottom: float
    height: float


@dataclass(frozen=True)
class BoxFigure(SolidFigure):
    """
    A rectangular box (cuboid). The figure can be rotated (meaning its walls don't have
    to be aligned with the axes of the coordinate system). The edge lengths are the final lengths of
    each edge, not the distance from the center of the figure (meaning they are full-size not half-size,
    for example: the edge lengths 1, 1, 1 will result in a 1 by 1 by 1 cube).
    """

    x_edge_length: float
    y_edge_length: float
    z_edge_length: float


def parse_figure(figure_dict: dict) -> SolidFigure:
    """Parse json containing information about figure to figure."""
    figure_type = figure_dict["userData"]["geometryType"]
    if figure_type == "CylinderGeometry":
        return CylinderFigure(uuid=figure_dict["uuid"],
                              position=tuple(figure_dict["userData"]["position"]),
                              rotation=tuple(figure_dict["userData"]["rotation"]),
                              radius_top=figure_dict["userData"]['parameters']["radiusTop"],
                              radius_bottom=figure_dict["userData"]['parameters']["radiusBottom"],
                              height=figure_dict["userData"]['parameters']["height"],
                              )
    if figure_type == "BoxGeometry":
        return BoxFigure(uuid=figure_dict["uuid"],
                         position=tuple(figure_dict["userData"]["position"]),
                         rotation=tuple(figure_dict["userData"]["rotation"]),
                         y_edge_length=figure_dict["userData"]['parameters']["height"],
                         x_edge_length=figure_dict["userData"]['parameters']["width"],
                         z_edge_length=figure_dict["userData"]['parameters']["depth"],
                         )
    if figure_type == "SphereGeometry":
        return SphereFigure(uuid=figure_dict["uuid"],
                            position=tuple(figure_dict["userData"]["position"]),
                            rotation=tuple(figure_dict["userData"]["rotation"]),
                            radius=figure_dict["userData"]['parameters']["radius"],
                            )

    print(f"Invalid figure type \"{figure_type}\".")
    raise ValueError("Parser type must be either 'CylinderGeometry', 'BoxGeometry' or 'SphereGeometry'")
