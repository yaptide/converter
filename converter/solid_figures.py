from dataclasses import dataclass, field
from abc import ABC


@dataclass(frozen=False)
class SolidFigure(ABC):
    """
    Abstract solid figure in 3D space. It is characterised by position in
    space and rotation along X,Y,Z axis in its own reference frame. Size of
    the figure (its extend in space) is defined in its subclasses.
    """

    uuid: str = "AAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA"

    position: tuple[float, float, float] = field(default_factory=lambda: [0., 0., 0.])
    rotation: tuple[float, float, float] = field(default_factory=lambda: [0., 0., 0.])

    def expand(self, expansion: float) -> None:
        """Expand figure by `expansion` in each dimension."""


@dataclass(frozen=False)
class SphereFigure(SolidFigure):
    """A sphere. Its size is defined by its radius."""

    radius: float = 1.

    def expand(self, expansion: float) -> None:
        """Expand figure by `expansion` in each dimension. Increases figures radius by `expansion`"""
        self.radius += expansion/2


@dataclass(frozen=False)
class CylinderFigure(SolidFigure):
    """
    A cylinder, a cone or a truncated cone. It's defined by the radii of both of
    its bases(top and bottom) and height. A cone can be created by setting one
    of the radii to zero.
    """

    radius_top: float = 1.
    radius_bottom: float = 1.
    height: float = 1.

    def expand(self, expansion: float) -> None:
        """
        Expand figure by `expansion` in each dimension. Increases figures height and both radi by `expansion`.
        """
        self.radius_top += expansion/2
        self.radius_bottom += expansion/2
        self.height += expansion


@dataclass(frozen=False)
class BoxFigure(SolidFigure):
    """
    A rectangular box (cuboid). The figure can be rotated (meaning its walls don't have
    to be aligned with the axes of the coordinate system). The edge lengths are the final lengths of
    each edge, not the distance from the center of the figure (meaning they are full-size not half-size,
    for example: the edge lengths 1, 1, 1 will result in a 1 by 1 by 1 cube).
    """

    x_edge_length: float = 1.
    y_edge_length: float = 1.
    z_edge_length: float = 1.

    def expand(self, expansion: float) -> None:
        """
        Expand figure by `expansion` in each dimension. Increases figures wieght, depth and height by `expansion`.
        """
        self.x_edge_length += expansion
        self.y_edge_length += expansion
        self.z_edge_length += expansion


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
