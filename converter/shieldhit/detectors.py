from dataclasses import dataclass
from abc import ABC


@dataclass(frozen=True)
class ScoringDetector(ABC):
    """Abstract geometry dataclass for DetectConfig."""

    uuid: str
    name: str


@dataclass(frozen=True)
class ScoringGlobal(ScoringDetector):
    r"""\"All\" detector. Scores on the whole defined space."""

    name: str

    template: str = """Geometry All
    Name {name}
"""

    def __str__(self) -> str:
        return self.template.format(name=self.name)


@dataclass(frozen=True)
class ScoringCylinder(ScoringDetector):
    """Cylinder detector dataclass used in DetectConfig."""

    name: str = "CylZ_Mesh"
    r_min: float = 0.
    r_max: float = 10.
    r_bins: int = 1
    h_min: float = 0.
    h_max: float = 20.
    h_bins: int = 400

    template: str = """Geometry Cyl
    Name {name}
    R {r_min:g} {r_max:g} {r_bins:d}
    Z {h_min:g} {h_max:g} {h_bins:d}
"""

    def __str__(self) -> str:
        return self.template.format(
            name=self.name,
            r_min=self.r_min, r_max=self.r_max, r_bins=self.r_bins,
            h_min=self.h_min, h_max=self.h_max, h_bins=self.h_bins,
        )


@dataclass(frozen=True)
class ScoringMesh(ScoringDetector):
    """Mesh detector dataclass used in DetectConfig."""

    name: str = "YZ_Mesh"
    x_min: float = -0.5
    x_max: float = 0.5
    x_bins: int = 1
    y_min: float = -2.
    y_max: float = 2.
    y_bins: int = 80
    z_min: float = 0.
    z_max: float = 20.
    z_bins: int = 400

    template: str = """Geometry Mesh
    Name {name}
    X {x_min:g} {x_max:g} {x_bins:d}
    Y {y_min:g} {y_max:g} {y_bins:d}
    Z {z_min:g} {z_max:g} {z_bins:d}
"""

    def __str__(self) -> str:
        return self.template.format(
            name=self.name,
            x_min=self.x_min, x_max=self.x_max, x_bins=self.x_bins,
            y_min=self.y_min, y_max=self.y_max, y_bins=self.y_bins,
            z_min=self.z_min, z_max=self.z_max, z_bins=self.z_bins,
        )


@dataclass(frozen=True)
class ScoringZone(ScoringDetector):
    """Scoring zone dataclass used un DetectConfig."""

    name: str
    first_zone_id: int
    last_zone_id: str = ""
    volume: float = 1.

    template: str = """Geometry Zone
    Name {name}
    Zone {first_zone} {last_zone}
    Volume {volume:f}
"""

    def __str__(self) -> str:
        return self.template.format(
            name=self.name,
            first_zone=self.first_zone_id, last_zone=self.last_zone_id,
            volume=self.volume,
        )
