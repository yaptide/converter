from typing import List, Dict, Any

def generate_histogram_lines(probe_histograms: List[Dict[str, Any]]) -> List[str]:
    """Append histogram output commands for all probe quantities."""
    lines: List[str] = []
    for idx, hist in enumerate(probe_histograms):
        qname = hist["quantity"]
        det_name = hist["detector"]
        arbitrary_name = f"{qname}_differential_{idx}"
        lines.append(
            f"/analysis/h1/create {qname}_{idx} {arbitrary_name} {hist['bins']} "
            f"{hist['min']} {hist['max']} {hist['unit']} {hist['XScale']} {hist['XBinScheme']}"
        )
        lines.append(f"/score/fill1D {idx} {det_name} {qname}")
    return lines
