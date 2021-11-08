from dataclasses import dataclass
from abc import ABC


@dataclass(frozen=True)
class SolidFigure(ABC):
    """Abstract figure, bodies are used to define geometries."""

    uuid: str
    offset: tuple[float, float, float]
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
    to be aligned with the axes of the coordinate system). Its size is defined by height, width and
    depth (which would represent Z, Y and X if not rotated) and the values represent the full 
    length of each edge (not half-length).
    """

    height: float
    width: float
    depth: float


def parse_figure(figure_dict: dict) -> SolidFigure:
    """Parse json containing information about figure to figure."""
    figure_type = figure_dict["userData"]["geometryType"]
    if figure_type == "CylinderGeometry":
        return CylinderFigure(uuid=figure_dict["uuid"],
                              offset=tuple(figure_dict["userData"]["position"]),
                              rotation=tuple(figure_dict["userData"]["rotation"]),
                              radius_top=figure_dict["userData"]['parameters']["radiusTop"],
                              radius_bottom=figure_dict["userData"]['parameters']["radiusBottom"],
                              height=figure_dict["userData"]['parameters']["height"],
                              )
    if figure_type == "BoxGeometry":
        return BoxFigure(uuid=figure_dict["uuid"],
                         offset=tuple(figure_dict["userData"]["position"]),
                         rotation=tuple(figure_dict["userData"]["rotation"]),
                         height=figure_dict["userData"]['parameters']["height"],
                         width=figure_dict["userData"]['parameters']["width"],
                         depth=figure_dict["userData"]['parameters']["depth"],
                         )
    if figure_type == "SphereGeometry":
        return SphereFigure(uuid=figure_dict["uuid"],
                            offset=tuple(figure_dict["userData"]["position"]),
                            rotation=tuple(figure_dict["userData"]["rotation"]),
                            radius=figure_dict["userData"]['parameters']["radius"],
                            )

    print(f"Invalid figure type \"{figure_type}\".")
    raise ValueError("Parser type must be either 'CylinderGeometry', 'BoxGeometry' or 'SphereGeometry'")
