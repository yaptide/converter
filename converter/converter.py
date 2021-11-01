from abc import ABC, abstractmethod, abstractproperty
from functools import reduce
from dataclasses import dataclass, field
from os import path


@dataclass(frozen=True)
class Geometry(ABC):
    """Abstract geometry dataclass for DetectConfig."""

    pass


@dataclass(order=True, frozen=True)
class Cylinder(Geometry):
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
class Mesh(Geometry):
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
class BeamConfig:
    """Class mapping of the beam.dat config file."""

    energy: float = 150.
    nstat: int = 1000

    beam_template: str = """
RNDSEED      	89736501     ! Random seed
JPART0       	2            ! Incident particle type
TMAX0      	{energy:3.6f}   0.0  ! Incident energy; (MeV/nucl)
NSTAT       {nstat:d}    -1 ! NSTAT, Step of saving
STRAGG          2            ! Straggling: 0-Off 1-Gauss, 2-Vavilov
MSCAT           2            ! Mult. scatt 0-Off 1-Gauss, 2-Moliere
NUCRE           0            ! Nucl.Reac. switcher: 1-ON, 0-OFF
"""

    def __str__(self) -> str:
        return self.beam_template.format(energy=self.energy, nstat=self.nstat)


@dataclass
class MatConfig:
    """Class mapping of the mat.dat config file."""

    materials: list[int] = field(default_factory=lambda: [276])

    material_template: str = """MEDIUM {idx:d}
ICRU {mat:d}
END
"""

    def __str__(self) -> str:
        material_strings = [self.material_template.format(idx=idx, mat=mat) for idx, mat in enumerate(self.materials)]
        return "\n".join(material_strings)


@dataclass
class DetectConfig:
    """Class mapping of the detect.dat config file."""

    geometries: list[Geometry] = field(default_factory=lambda: [Cylinder(id=0), Mesh(id=0)])

    detect_template = """Output
    Filename mesh.bdo
    Geo ScoringCylinder
    Quantity Dose
    """

    def __str__(self):
        detect_strings = [str(geo)
                          for geo in self.geometries] + [self.detect_template]
        return "\n".join(detect_strings)


@dataclass
class GeoConfig:
    """Class mapping of the geo.dat config file."""

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

    def __str__(self) -> str:
        return self.geo_template


class Parser(ABC):
    """Abstract parser, the template for implementing other parsers."""

    @abstractmethod
    def parse_configs(json: dict):
        """Convert the json dict to the 4 config dataclasses."""
        pass

    @abstractmethod
    def save_configs(target_dir_path: str):
        """
        Save the configs as text files in the target_dir.
        The files are: beam.dat, mat.dat, detect.dat and geo.dat.
        """
        pass


class DummmyParser(Parser):
    """A simple placeholder parser that ignores the json input and prints example (default) configs."""

    def __init__(self) -> None:
        self.beam_config = BeamConfig()
        self.mat_config = MatConfig()
        self.detect_config = DetectConfig()
        self.geo_config = GeoConfig()

    def parse_configs(self, json: dict):
        """Basicaly do nothing since we work on defaults in this parser."""
        pass

    def save_configs(self, target_dir: str):
        """
        Save the configs as text files in the target_dir.
        The files are: beam.dat, mat.dat, detect.dat and geo.dat.
        """
        target_dir = path.abspath(target_dir)

        with open(path.join(target_dir, 'beam.dat'), 'x') as beam_f:
            beam_f.write(str(self.beam_config))

        with open(path.join(target_dir, 'mat.dat'), 'x') as mat_f:
            mat_f.write(str(self.mat_config))

        with open(path.join(target_dir, 'detect.dat'), 'x') as detect_f:
            detect_f.write(str(self.detect_config))

        with open(path.join(target_dir, 'geo.dat'), 'x') as geo_f:
            geo_f.write(str(self.geo_config))


class JustParser(Parser):
    """A parser :)"""


class Runner:
    """Converts input data dict to files that will be saved in output_dir using the specified parser."""

    def __init__(self, parser: Parser, input_data: dict, output_dir: str) -> None:
        self.parser = parser
        self.input_data = input_data
        self.output_dir = output_dir

    def run_parser(self) -> None:
        """Convert the configs and save them in the output_dir directory."""
        self.parser.parse_configs(self.input_data)
        self.parser.save_configs(self.output_dir)
