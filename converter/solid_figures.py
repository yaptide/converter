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

    def expand(self, margin: float) -> None:
        """Expand figure by `expansion` in each dimension."""


@dataclass(frozen=False)
class SphereFigure(SolidFigure):
    """A sphere. Its size is defined by its radius."""

    radius: float = 1.

    def expand(self, margin: float) -> None:
        """Expand figure by `margin` in each dimension. Increases figure radius by adding to it a `margin`"""
        self.radius += margin


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

    def expand(self, margin: float) -> None:
        """
        Expand the figure by `margin` in each dimension.
        Increases figures height by 2 * `margin` (to achieve the same expansion by 1 * `margin` on the
        bottom and top side.
        Increase as well bottom and top radius by 1 * `margin`.
        """
        self.radius_top += margin
        self.radius_bottom += margin
        self.height += margin * 2


@dataclass(frozen=False)
class BoxFigure(SolidFigure):
    """
    A rectangular box (cuboid). The figure can be rotated (meaning its walls don't have
    to be aligned with the axes of the coordinate system). The edge lengths are the final lengths of
    each edge, not the distance from the center of the figure (meaning they are full-size not hageometryDatalf-size,
    for example: the edge lengths 1, 1, 1 will result in a 1 by 1 by 1 cube).
    """

    x_edge_length: float = 1.
    y_edge_length: float = 1.
    z_edge_length: float = 1.

    def expand(self, margin: float) -> None:
        """
        Expand the figure by `margin` in each dimension.
        Increases figures weight, depth and height by 2 * `margin` to achieve the same
        expansion (1 * `margin`) on each side.
        """
        self.x_edge_length += margin * 2
        self.y_edge_length += margin * 2
        self.z_edge_length += margin * 2


def parse_figure(figure_dict: dict) -> SolidFigure:
    """Parse json containing information about figure to figure."""
    figure_type = figure_dict["geometryData"]["geometryType"]
    if figure_type == "CylinderGeometry":
        return CylinderFigure(
            uuid=figure_dict["uuid"],
            position=tuple(figure_dict["geometryData"]["position"]),
            rotation=tuple(figure_dict["geometryData"]["rotation"]),
            radius_top=figure_dict["geometryData"]['parameters']["radius"],
            radius_bottom=figure_dict["geometryData"]['parameters']["radius"],
            height=figure_dict["geometryData"]['parameters']["depth"],
        )
    if figure_type == "BoxGeometry":
        return BoxFigure(
            uuid=figure_dict["uuid"],
            position=tuple(figure_dict["geometryData"]["position"]),
            rotation=tuple(figure_dict["geometryData"]["rotation"]),
            y_edge_length=figure_dict["geometryData"]['parameters']["height"],
            x_edge_length=figure_dict["geometryData"]['parameters']["width"],
            z_edge_length=figure_dict["geometryData"]['parameters']["depth"],
        )
    if figure_type == "SphereGeometry":
        return SphereFigure(
            uuid=figure_dict["uuid"],
            position=tuple(figure_dict["geometryData"]["position"]),
            rotation=tuple(figure_dict["geometryData"]["rotation"]),
            radius=figure_dict["geometryData"]['parameters']["radius"],
        )

    print(f"Invalid figure type \"{figure_type}\".")
    raise ValueError("Parser type must be either 'CylinderGeometry', 'BoxGeometry' or 'SphereGeometry'")
