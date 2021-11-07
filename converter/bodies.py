from dataclasses import dataclass
from abc import ABC


@dataclass(frozen=True)
class Body(ABC):
    """Abstract body, bodies are used to define geometries."""

    uuid: str
    x_offset: float
    y_offset: float
    z_offset: float


@dataclass(frozen=True)
class SphereBody(Body):
    """A sphere body. It's defined by its radius, offset from the point (0, 0, 0) xyz and its rotation along each axis."""

    radius: float


@dataclass(frozen=True)
class CylinderBody(Body):
    """
    A cylinder body. It's defined by the radii of both of its bases(top and bottom),
    its height, its offset from the point (0, 0, 0) xyz and its rotation along each axis.
    """

    radius_top: float
    radius_bottom: float
    height: float


@dataclass(frozen=True)
class BoxBody(Body):
    """
    A box body. It's defined by size in the 3 dimensions (z - height, x - width and y - depth), 
    its offset from the point (0, 0, 0) xyz and its rotation along each axis.
    """
    height: float
    width: float
    depth: float


def parse_body(body_dict: dict) -> Body:
    pass
