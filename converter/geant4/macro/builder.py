from typing import Dict
from .beam_parser import generate_beam_lines
from .scoring_parser import generate_scoring_lines
from .histogram_parser import generate_histogram_lines
from .run_parser import generate_run_lines
from .result_parser import generate_result_lines

def generate_macro_entry_point(data: Dict) -> str:
    """Central builder for Geant4 macro, combining all parsers."""

    lines = []

    # Beam
    lines.extend(generate_beam_lines(data))

    # Scoring
    scoring_lines, probe_histograms = generate_scoring_lines(data)
    lines.extend(scoring_lines)

    # Histogram
    lines.extend(generate_histogram_lines(probe_histograms))

    # Run
    lines.extend(generate_run_lines(data))

    # Results
    lines.extend(generate_result_lines(data))

    return "\n".join(lines)