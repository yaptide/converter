from typing import Dict, Any, List
from .beam_parser import BeamParser
from .scoring_parser import ScoringParser
from .histogram_parser import HistogramParser
from .run_parser import RunParser
from .result_parser import ResultParser


class Geant4MacroBuilder:
    """Central builder for Geant4 macro, combining all parsers."""

    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data
        self.lines: List[str] = []
        self.probe_histograms: List[Dict[str, Any]] = []

    def generate(self) -> str:
        """Generate a complete GEANT4 macro file."""
        BeamParser(self.data, self.lines).parse()

        scoring = ScoringParser(self.data, self.lines)

        scoring.parse()

        self.probe_histograms = scoring.probe_histograms

        HistogramParser(self.probe_histograms, self.lines).parse()

        RunParser(self.data, self.lines).parse()

        ResultParser(self.data, self.lines).parse()

        return "\n".join(self.lines)
