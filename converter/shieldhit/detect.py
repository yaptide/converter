from dataclasses import dataclass, field
from abc import ABC


@dataclass(frozen=True)
class ScoringGeometry(ABC):
    """Abstract geometry dataclass for DetectConfig."""


@dataclass(order=True, frozen=True)
class ScoringCylinder(ScoringGeometry):
    """Cylinder geometry dataclass used in DetectConfig."""

    sort_index: int = field(init=False)

    id: str
    radius: int = 1
    height: int = 400

    template: str = """Geometry Cyl
    Name ScoringCylinder
    R 0.0 10.0 {cyl_nr:d}
    Z 0.0 30.0 {cyl_nz:d}"""

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.id)

    def __str__(self) -> str:
        return self.template.format(cyl_nr=self.radius, cyl_nz=self.height)


@dataclass(order=True, frozen=True)
class ScoringMesh(ScoringGeometry):
    """Mesh geometry dataclass used in DetectConfig."""

    sort_index: int = field(init=False)

    id: str
    x: int = 1
    y: int = 100
    z: int = 300

    template: str = """Geometry Mesh
    Name MyMesh_YZ
    X -5.0  5.0    {mesh_nx:d}
    Y -5.0  5.0    {mesh_ny:d}
    Z  0.0  30.0   {mesh_nz:d}"""

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.id)

    def __str__(self) -> str:
        return self.template.format(mesh_nx=self.x, mesh_ny=self.y, mesh_nz=self.z)


@dataclass
class DetectConfig:
    """Class mapping of the detect.dat config file."""

    detect_template = """Geometry Cyl
    Name CylZ_Mesh
    R  0.0  10.0    1
    Z  0.0  20.0    400

Geometry Mesh
    Name YZ_Mesh
    X -0.5  0.5    1
    Y -2.0  2.0    80
    Z  0.0  20.0   400


Output
    Filename cylz.bdo
    Geo CylZ_Mesh
    Quantity DoseGy

Output
    Filename yzmsh.bdo
    Geo YZ_Mesh
    Quantity DoseGy
    """

    def __str__(self):
        return self.detect_template
