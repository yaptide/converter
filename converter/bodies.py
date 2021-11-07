from dataclasses import dataclass
from abc import ABC


@dataclass(frozen=True)
class Body(ABC):
    """Abstract body, bodies are used to define geometries."""

    uuid: str
    x_offset: float
    y_offset: float
    z_offset: float
    x_rotation: float
    y_rotation: float
    z_rotation: float


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
    type = body_dict["userData"]["geometryType"]
    if type == "CylinderGeometry":
        return CylinderBody(uuid=body_dict["uuid"],
                            x_offset=body_dict["userData"]["position"][0],
                            y_offset=body_dict["userData"]["position"][1],
                            z_offset=body_dict["userData"]["position"][2],
                            x_rotation=body_dict["userData"]["rotation"][0],
                            y_rotation=body_dict["userData"]["rotation"][1],
                            z_rotation=body_dict["userData"]["rotation"][2],
                            radius_top=body_dict["userData"]['parameters']["radiusTop"],
                            radius_bottom=body_dict["userData"]['parameters']["radiusBottom"],
                            height=body_dict["userData"]['parameters']["height"],
                            )
    if type == "BoxGeometry":
        return BoxBody(uuid=body_dict["uuid"],
                       x_offset=body_dict["userData"]["position"][0],
                       y_offset=body_dict["userData"]["position"][1],
                       z_offset=body_dict["userData"]["position"][2],
                       x_rotation=body_dict["userData"]["rotation"][0],
                       y_rotation=body_dict["userData"]["rotation"][1],
                       z_rotation=body_dict["userData"]["rotation"][2],
                       height=body_dict["userData"]['parameters']["height"],
                       width=body_dict["userData"]['parameters']["width"],
                       depth=body_dict["userData"]['parameters']["depth"],
                       )
    if type == "SphereGeometry":
        return SphereBody(uuid=body_dict["uuid"],
                          x_offset=body_dict["userData"]["position"][0],
                          y_offset=body_dict["userData"]["position"][1],
                          z_offset=body_dict["userData"]["position"][2],
                          x_rotation=body_dict["userData"]["rotation"][0],
                          y_rotation=body_dict["userData"]["rotation"][1],
                          z_rotation=body_dict["userData"]["rotation"][2],
                          radius=body_dict["userData"]['parameters']["radius"],
                          )

    print(f"Invalid body type \"{type}\".")
    raise ValueError("Parser type must be either 'CylinderGeometry', 'BoxGeometry' or 'SphereGeometry'")
