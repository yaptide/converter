from typing import Dict, List


def generate_run_lines(data: Dict) -> List[str]:
    """Generate run section."""
    lines: List[str] = []
    beam = data.get("beam", {})
    lines.extend([
        "\n##########################################",
        "################## Run ###################",
        "##########################################\n",
        f"/run/beamOn {beam.get('numberOfParticles', 10000)}\n"
    ])

    return lines
