from abc import ABC, abstractmethod, abstractproperty
from functools import reduce


class Geometry(ABC):
    pass


class Cylinder(Geometry):
    template: str = """Geometry Cyl
    Name ScoringCylinder
    R 0.0 10.0 {cyl_nr:d}
    Z 0.0 30.0 {cyl_nz:d}"""

    def __init__(self, radius=10, height=10):
        self.radius = radius
        self.height = height

    def __str__(self) -> str:
        return self.template.format(cyl_nr=self.radius, cyl_nz=self.height)


class Mesh(Geometry):
    template: str = """Geometry Mesh
    Name MyMesh_YZ
    X -5.0  5.0    {mesh_nx:d}
    Y -5.0  5.0    {mesh_ny:d}
    Z  0.0  30.0   {mesh_nz:d}"""

    def __init__(self, x=10, y=10, z=10):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return self.template.format(mesh_nx=self.x, mesh_ny=self.y, mesh_nz=self.z)


class BeamConfig:
    """Class mapping of the beam.dat config file"""

    beam_template: str = """
RNDSEED      	89736501     ! Random seed
JPART0       	2            ! Incident particle type
TMAX0      	{energy:3.6f}   0.0  ! Incident energy; (MeV/nucl)
NSTAT       {nstat:d}    -1 ! NSTAT, Step of saving
STRAGG          2            ! Straggling: 0-Off 1-Gauss, 2-Vavilov
MSCAT           2            ! Mult. scatt 0-Off 1-Gauss, 2-Moliere
NUCRE           0            ! Nucl.Reac. switcher: 1-ON, 0-OFF
"""

    def __init__(self, energy: float = 250., nstat: int = 10000):
        self.energy = energy
        self.nstat = nstat

    def __str__(self) -> str:
        return self.beam_template.format(energy=self.energy, nstat=self.nstat)


class MatConfig:
    """Class mapping of the mat.dat config file"""

    material_template: str = """MEDIUM {idx}
ICRU {mat}
END
"""

    def __init__(self, materials: list[int] = [276]):
        self.materials: list[str] = materials

    def __str__(self) -> str:
        material_strings = [self.material_template.format(
            idx=idx, mat=mat) for idx, mat in enumerate(self.materials)]
        return "\n".join(material_strings)


class DetectConfig:
    """Class mapping of the detect.dat config file"""
    detect_template = """Output
    Filename mesh.bdo
    Geo ScoringCylinder
    Quantity Dose
    """

    def __init__(self, geometries: list[Geometry] = [Cylinder(), Mesh()]):
        self.geometries: Geometry = geometries

    def __str__(self):
        detect_strings = [str(geo)
                          for geo in self.geometries] + [self.detect_template]
        return "\n".join(detect_strings)


class GeoConfig:
    # TODO: Parametrize this
    """Class mapping of the geo.dat config file"""

    geo_template: str = """
*---><---><--------><------------------------------------------------>
    0    0           protons, H2O 30 cm cylinder, r=10, 1 zone
*---><---><--------><--------><--------><--------><--------><-------->
  RCC    1       0.0       0.0       0.0       0.0       0.0      30.0
                10.0
  RCC    2       0.0       0.0      -5.0       0.0       0.0      35.0
                15.0
  RCC    3       0.0       0.0     -10.0       0.0       0.0      40.0
                20.0
  END
  001          +1
  002          +2     -1
  003          +3     -2
  END
* material codes: 1 - liquid water (ICRU material no 276), 1000 - vacuum, 0 - black body
    1    2    3
    1 1000    0
"""

    def __init__(self):
        pass

    def __str__(self) -> str:
        return self.geo_template
