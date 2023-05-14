from dataclasses import dataclass, field
from typing import Optional
from converter.shieldhit.scoring_geometries import ScoringGeometry, ScoringCylinder, ScoringMesh


@dataclass
class ScoringFilter:
    """Dataclass storing information about simulation output. Used in DetectConfig dataclass."""

    uuid: str

    name: str
    rules: list[tuple[str, str, int]]

    rule_template: str = """
    {0} {1} {2}"""

    template: str = """Filter
    Name {name}{rules}"""

    def __str__(self) -> str:
        return self.template.format(name=self.name,
                                    rules=''.join([self.rule_template.format(*rule) for rule in self.rules]))


@dataclass
class OutputQuantity:
    """Class for storing output quantities used in detect."""

    detector_type: str
    filter_name: str = ""
    diff1: Optional[tuple[float, float, float, str]] = None
    diff1_t: Optional[str] = None
    diff2: Optional[tuple[float, float, float, str]] = None
    diff2_t: Optional[str] = None

    quantity_template: str = """
    Quantity {detector_type} {filter_name}"""
    diff_template = """
    Diff{0} {d[0]} {d[1]} {d[2]} {log}
    Diff{0}Type {diff_t}"""

    def __str__(self) -> str:
        return ''.join([
            self.quantity_template.format(detector_type=self.detector_type, filter_name=self.filter_name),
            self.diff_template.format(1, d=self.diff1, diff_t=self.diff1_t, log=("log" if self.diff1[3] else ""))
            if self.diff1 else "",
            self.diff_template.format(2, d=self.diff2, diff_t=self.diff2_t) if self.diff2 else "",
        ])


@dataclass
class ScoringOutput:
    """Dataclass storing information about shieldhit scoring outputs."""

    filename: Optional[str] = None
    fileformat: Optional[str] = None
    geometry: Optional[str] = None
    medium: Optional[str] = None
    offset: Optional[float] = None
    primaries: Optional[int] = None
    quantities: list[OutputQuantity] = field(default_factory=lambda: [])
    rescale: Optional[float] = None

    filename_str_template: str = """
    Filename {filename}"""
    fileformat_str_template: str = """
    Fileformat {fileformat}"""
    geometry_str_template: str = """
    Geo {geometry}"""
    medium_str_template: str = """
    Medium {medium}"""
    offset_str_template: str = """
    Offset {offset:e}"""
    primaries_str_template: str = """
    Primaries {primaries:e}"""
    rescale_str_template: str = """
    Rescale {rescale:e}"""

    template: str = """Output{fields}"""

    def __str__(self) -> str:
        return self.template.format(fields=''.join([
            self.filename_str_template.format(filename=self.filename) if self.filename else "",
            self.fileformat_str_template.format(fileformat=self.fileformat) if self.fileformat else "",
            self.geometry_str_template.format(geometry=self.geometry) if self.geometry else "",
            self.medium_str_template.format(medium=self.medium) if self.medium else "",
            self.offset_str_template.format(offset=self.offset) if self.offset else "",
            self.primaries_str_template.format(primaries=self.primaries) if self.primaries else "", ''.join(
                [str(quantity) for quantity in self.quantities]),
            self.rescale_str_template.format(rescale=self.rescale) if self.rescale else "", "\n"
        ]))


@dataclass
class DetectConfig:
    """Class mapping of the detect.dat config file."""

    scoring_geometries: list[ScoringGeometry] = field(default_factory=lambda: [
        ScoringCylinder(""),
        ScoringMesh(""),
    ])

    scoring_filters: list[ScoringFilter] = field(default_factory=lambda: [])

    scoring_outputs: list[ScoringOutput] = field(default_factory=lambda: [
        ScoringOutput("cylz.bdo", geometry="CylZ_Mesh", quantities=[OutputQuantity("DoseGy")]),
        ScoringOutput("yzmsh.bdo", geometry="YZ_Mesh", quantities=[OutputQuantity("DoseGy")]),
    ])

    def __str__(self):
        return '\n'.join([
            "\n".join([str(geom) for geom in self.scoring_geometries]),
            "\n".join([str(filter) for filter in self.scoring_filters]),
            "\n".join([str(output) for output in self.scoring_outputs]),
        ])
