from typing import Dict, Any, List
from converter.common import convert_beam_energy
from converter.geant4.constants import GEANT4_PARTICLE_MAP, HEAVY_ION_PARTICLE_ID


class BeamParser:
    """Generate beam initialization section."""

    def __init__(self, data: Dict[str, Any], lines: List[str]) -> None:
        self.data = data
        self.lines = lines

    def parse(self) -> None:
        """Parse the beam configuration and append GEANT4 /gps commands."""
        beam = self.data.get("beam", {})
        particle = beam.get("particle", {})

        particle_id = particle.get("id", 2)
        pos = beam.get("position", [0, 0, 0])
        direction = beam.get("direction", [0, 0, 1])

        a = particle.get("a", 1)
        z = particle.get("z", a)

        energy_lines = self._compute_energy(beam, particle_id, a, direction)

        self.lines.extend(
            self._particle_commands(particle_id, a, z, pos)
        )

        self._append_beam_shape(beam)

        self.lines.extend(energy_lines)

    def _particle_commands(self, particle_id: int, a: int, z: int, pos: List[float]) -> List[str]:
        """Return GEANT4 header + particle commands."""
        header = [
            "/run/initialize\n",
            "##########################################",
            "####### Particle Source definition #######",
            "##########################################\n",
            "/gps/verbose 0",
            f"/gps/position {pos[0]} {pos[1]} {pos[2]} cm"
        ]

        if particle_id == HEAVY_ION_PARTICLE_ID:
            particle_cmd = [
                "/gps/particle ion",
                f"/gps/ion {z} {a} 0 0",
            ]
        else:
            if particle_id not in GEANT4_PARTICLE_MAP or "name" not in GEANT4_PARTICLE_MAP[particle_id]:
                raise ValueError(f"Invalid particle id={particle_id}")

            name = GEANT4_PARTICLE_MAP[particle_id]["name"]
            particle_cmd = [f"/gps/particle {name}"]

        return header + particle_cmd

    def _compute_energy(self, beam: Dict[str, Any], particle_id: int, a: int, direction: List[float]) -> List[str]:
        """Compute energy values *and* return ready-to-append /gps output lines."""
        input_energy = beam.get("energy", 0)
        unit = beam.get("energyUnit", "MeV")

        energy, _, scale = convert_beam_energy(
            GEANT4_PARTICLE_MAP, particle_id, a, input_energy, unit
        )

        sigma = beam.get("energySpread", 0) * scale
        high = beam.get("energyHighCutoff", 1000) * scale
        low = beam.get("energyLowCutoff", 0) * scale

        return [
            f"/gps/direction {direction[0]} {direction[1]} {direction[2]}",
            "/gps/ene/type Gauss",
            f"/gps/ene/mono {energy} MeV",
            f"/gps/ene/sigma {sigma} MeV",
            f"/gps/ene/max {high} MeV",
            f"/gps/ene/min {low} MeV",
        ]

    def _append_beam_shape(self, beam: Dict[str, Any]) -> None:
        """Append commands describing the beam's spatial distribution."""
        shape_data = beam.get("sigma", {})
        shape_type = shape_data.get("type", None)
        x = shape_data.get("x", 0)
        y = shape_data.get("y", 0)
        if shape_type == "Flat circular":
            self.lines.append("/gps/pos/type Plane")
            self.lines.append("/gps/pos/shape Circle")
            if y > 0:
                self.lines.append(f"/gps/pos/radius {y} cm")
        elif shape_type == "Flat square":
            self.lines.append("/gps/pos/type Plane")
            self.lines.append("/gps/pos/shape Rectangle")
            if x > 0:
                self.lines.append(f"/gps/pos/halfx {x} cm")
            if y > 0:
                self.lines.append(f"/gps/pos/halfy {y} cm")
        else:
            self.lines.append("/gps/pos/type Beam")
            if x > 0:
                self.lines.append(f"/gps/pos/sigma_x {x} cm")
            if y > 0:
                self.lines.append(f"/gps/pos/sigma_y {y} cm")
