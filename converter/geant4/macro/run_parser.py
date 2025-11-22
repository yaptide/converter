from typing import Dict, Any, List

class RunParser:
    """Generate run section."""


    def __init__(self, data: Dict[str, Any], lines: List[str]):
        self.data = data
        self.lines = lines

    def parse(self):
        """Generate /run and /event commands based on configuration."""
        beam = self.data.get("beam", {})
        self.lines.extend([
            "\n##########################################",
            "################## Run ###################",
            "##########################################\n",
            f"/run/beamOn {beam.get('numberOfParticles', 10000)}\n"
        ])
