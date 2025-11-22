from typing import List, Dict, Any

class HistogramParser:
    """Generate histogram section for probes."""


    def __init__(self, probe_histograms: List[Dict[str, Any]], lines: List[str]) -> None:
        self.probe_histograms = probe_histograms
        self.lines = lines
        self.probe_counter = 0

    def parse(self) -> None:
        """Append histogram output commands for all probe quantities."""
        for hist in self.probe_histograms:
            qname = hist["quantity"]
            det_name = hist["detector"]
            arbitrary_name = f"{qname}_differential_{self.probe_counter}"
            self.lines.append(
                f"/analysis/h1/create {qname}_{self.probe_counter} {arbitrary_name} {hist['bins']} "
                f"{hist['min']} {hist['max']} {hist['unit']} {hist['XScale']} {hist['XBinScheme']}"
            )
            self.lines.append(f"/score/fill1D {self.probe_counter} {det_name} {qname}")
            self.probe_counter += 1
