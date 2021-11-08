from dataclasses import dataclass
from abc import ABC


@dataclass(frozen=True)
class SolidFigure(ABC):
    """Abstract figure, bodies are used to define geometries."""

    uuid: str
    offset: list[float]
    rotation: list[float]


@dataclass(frozen=True)
class SphereFigure(SolidFigure):
    """
    A sphere figure. It's defined by its radius, offset from the point (0, 0, 0) xyz
    and its rotation along each axis.
    """

    radius: float


@dataclass(frozen=True)
class CylinderFigure(SolidFigure):
    """
    A cylinder figure. It's defined by the radii of both of its bases(top and bottom),
    its height, its offset from the point (0, 0, 0) xyz and its rotation along each axis.
    """

    radius_top: float
    radius_bottom: float
    height: float


@dataclass(frozen=True)
class BoxFigure(SolidFigure):
    """
    A box figure. It's defined by size in the 3 dimensions (z - height, x - width and y - depth),
    its offset from the point (0, 0, 0) xyz and its rotation along each axis.
    """

    height: float
    width: float
    depth: float


def parse_figure(figure_dict: dict) -> SolidFigure:
    """Parse json containing information about figure to figure."""
    figure_type = figure_dict["userData"]["geometryType"]
    if figure_type == "CylinderGeometry":
        return CylinderFigure(uuid=figure_dict["uuid"],
                              offset=figure_dict["userData"]["position"],
                              rotation=figure_dict["userData"]["rotation"],
                              radius_top=figure_dict["userData"]['parameters']["radiusTop"],
                              radius_bottom=figure_dict["userData"]['parameters']["radiusBottom"],
                              height=figure_dict["userData"]['parameters']["height"],
                              )
    if figure_type == "BoxGeometry":
        return BoxFigure(uuid=figure_dict["uuid"],
                         offset=figure_dict["userData"]["position"],
                         rotation=figure_dict["userData"]["rotation"],
                         height=figure_dict["userData"]['parameters']["height"],
                         width=figure_dict["userData"]['parameters']["width"],
                         depth=figure_dict["userData"]['parameters']["depth"],
                         )
    if figure_type == "SphereGeometry":
        return SphereFigure(uuid=figure_dict["uuid"],
                            offset=figure_dict["userData"]["position"],
                            rotation=figure_dict["userData"]["rotation"],
                            radius=figure_dict["userData"]['parameters']["radius"],
                            )

    print(f"Invalid figure type \"{figure_type}\".")
    raise ValueError("Parser type must be either 'CylinderGeometry', 'BoxGeometry' or 'SphereGeometry'")
