import converter.geant4.utils as utils
from typing import Dict, Any, List

# skipcq: PYL-W0511
# TODO geantino names needs better mapping or handling
GEANT4_PARTICLE_MAP = {
    1: "neutron",
    2: "proton",
    3: "geantino",
    4: "e-",
    5: "e+",
    6: "alpha",
    7: "mu-",
    8: "mu+",
    9: "pi-",
    10: "pi+",
    11: "geantino",
}

GEANT4_QUANTITY_MAP = {
    "DoseGy": "doseDeposit",
    "Energy": "energyDeposit",
    "Fluence": "cellFlux",
    "KineticEnergySpectrum": "cellFlux",
}


class Geant4MacroGenerator:
    """Generate Geant4 mac (beam + scoring + run)."""

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize with JSON data."""
        self.data = data
        self.lines: List[str] = []
        self.probe_histograms: List[Dict[str, Any]] = []
        self.probe_counter = 0

    def generate(self) -> str:
        """Generate full Geant4 macro content."""
        self._append_initialization()
        self._append_scoring()
        self._append_histograms()
        self._append_run()
        self._append_results()
        return "\n".join(self.lines)

    def _append_initialization(self) -> None:
        """Append particle source and run initialization."""
        beam = self.data.get("beam", {})
        particle = beam.get("particle", {}).get("id", "2")
        pos = beam.get("position", [0, 0, 0])
        direction = beam.get("direction", [0, 0, 1])
        energy = beam.get("energy", 1)
        sigma = beam.get("energySpread", 0)
        energy_high = beam.get("energyHighCutoff", 1000)
        energy_min = beam.get("energyLowCutoff", 0)

        self.lines.extend([
            "/run/initialize\n",
            "##########################################",
            "####### Particle Source definition #######",
            "##########################################\n",
            "/gps/verbose 0",
            f"/gps/particle {GEANT4_PARTICLE_MAP.get(particle)}",
            f"/gps/position {pos[0]} {pos[1]} {pos[2]} cm",
            "/gps/pos/type Beam",
            f"/gps/direction {direction[0]} {direction[1]} {direction[2]}",
            "/gps/ene/type Gauss",
            f"/gps/ene/mono {energy} MeV",
            f"/gps/ene/sigma {sigma} MeV",
            f"/gps/ene/max {energy_high} MeV\n"
            f"/gps/ene/min {energy_min} MeV\n"
        ])

    # -------------------- Scoring --------------------
    def _append_scoring(self) -> None:
        """Append all detector scoring blocks."""
        self.lines.extend([
            "##########################################",
            "################ Scoring #################",
            "##########################################\n"
        ])

        detectors = {d["uuid"]: d for d in self.data.get("detectorManager", {}).get("detectors", [])}
        outputs = self.data.get("scoringManager", {}).get("outputs", [])
        filters = {f["uuid"]: f for f in self.data.get("scoringManager", {}).get("filters", [])}

        detector_quantities: Dict[str, List[Dict[str, Any]]] = {}
        for output in outputs:
            detector_uuid = output.get("detectorUuid")
            detector_quantities.setdefault(detector_uuid, []).extend(output.get("quantities", []))

        for detector_uuid, quantities in detector_quantities.items():
            detector = detectors.get(detector_uuid)
            if not detector:
                continue
            self._append_detector_scoring(detector, quantities, filters)

    def _append_detector_scoring(self, detector: Dict[str, Any], quantities: List[Dict[str, Any]],
                                 filters: Dict[str, Any]) -> None:
        """Append scoring for a single detector including mesh/probe and quantities."""
        name = utils.get_detector_name(detector)
        geom = detector.get("geometryData", {})
        geom_type = geom.get("geometryType", "Box")
        params = geom.get("parameters", {})
        pos_det = geom.get("position", [0, 0, 0])

        is_probe = any(q.get("keyword") == "KineticEnergySpectrum" for q in quantities)

        if is_probe:
            self._append_probe(detector, geom_type, params, pos_det)
        else:
            self._append_mesh(detector, geom_type, params, pos_det)

        for quantity in quantities:
            self._append_quantity(quantity, filters, name)

        self.lines.append("/score/close\n")

    def _append_mesh(self, detector: Dict[str, Any], geom_type: str,
                     params: Dict[str, Any], pos_det: List[float]) -> None:
        """Append a mesh (cylinder or box) for a detector, if it's not a cylinder box will be added"""
        name = utils.get_detector_name(detector)
        if geom_type.lower() in ["cyl", "cylinder"]:
            self.lines.append(f"/score/create/cylinderMesh {name}")
            self.lines.append(f"/score/mesh/locate {pos_det[0]} {pos_det[1]} {pos_det[2]} cm")
            radius = params.get("radius", 1)
            depth = params.get("depth", 1)
            n_radial = params.get("radialSegments", 1)
            n_z = params.get("zSegments", 1)
            self.lines.append(f"/score/mesh/cylinderSize {radius} {depth} cm")
            self.lines.append(f"/score/mesh/nBin {n_radial} {n_z} 1")
        else:
            self.lines.append(f"/score/create/boxMesh {name}")
            self.lines.append(f"/score/mesh/locate {pos_det[0]} {pos_det[1]} {pos_det[2]} cm")
            width = params.get("width", 1)
            height = params.get("height", 1)
            depth = params.get("depth", 1)
            n_x = params.get("xSegments", 1)
            n_y = params.get("ySegments", 1)
            n_z = params.get("zSegments", 1)
            self.lines.append(f"/score/mesh/boxSize {width} {height} {depth} cm")
            self.lines.append(f"/score/mesh/nBin {n_x} {n_y} {n_z}")

    def _append_probe(self, detector: Dict[str, Any], geom_type: str,
                      params: Dict[str, Any], pos_det: List[float]) -> None:
        """Append a probe scoring for KineticEnergySpectrum quantities."""
        name = utils.get_detector_name(detector)
        size = params.get("radius", 1) if geom_type.lower() in ["cyl", "cylinder"] \
            else max(params.get("width", 1), params.get("height", 1), params.get("depth", 1))
        self.lines.append(f"/score/create/probe {name} {size} cm")
        self.lines.append(f"/score/probe/locate {pos_det[0]} {pos_det[1]} {pos_det[2]} cm")

    def _append_quantity(self, quantity: Dict[str, Any], filters: Dict[str, Any], detector_name: str) -> None:
        """Append a quantity and its filter for a detector."""
        keyword = quantity.get("keyword", "")
        qname = quantity.get("name", keyword)
        mapped_keyword = GEANT4_QUANTITY_MAP.get(keyword, keyword.lower())
        self.lines.append(f"/score/quantity/{mapped_keyword} {qname}")

        if keyword == "KineticEnergySpectrum":
            self.probe_histograms.append({
                "quantity": qname,
                "detector": detector_name,
                "bins": quantity.get("histogramNBins", 1),
                "min": quantity.get("histogramMin", 0),
                "max": quantity.get("histogramMax", 1),
                "unit": quantity.get("histogramUnit", "MeV"),
                "XScale": quantity.get("histogramXScale", "none"),
                "XBinScheme": quantity.get("histogramXBinScheme", "linear"),
            })

        filter_uuid = quantity.get("filter")
        if filter_uuid and filter_uuid in filters:
            filter_particles = filters[filter_uuid]
            particle_types = filter_particles.get("data", {}).get("particleTypes", [])
            if particle_types:
                particle_names = " ".join([GEANT4_PARTICLE_MAP.get(pt["id"], pt["name"]) for pt in particle_types])
                self.lines.append(f"/score/filter/particle {filter_particles['name']} {particle_names}")

    # -------------------- The histogram for KineticEnergySpectrum --------------------
    def _append_histograms(self) -> None:
        """Append a histogram for KineticEnergySpectrum probe"""
        for hist in self.probe_histograms:
            qname = hist["quantity"]
            det_name = hist["detector"]
            arbitrary_name = f"{qname}_differential_{self.probe_counter}"
            self.lines.append(f"/analysis/h1/create {qname}_{self.probe_counter} {arbitrary_name} {hist['bins']} "
                              f"{hist['min']} {hist['max']} {hist['unit']} {hist['XScale']} {hist['XBinScheme']}")
            self.lines.append(f"/score/fill1D {self.probe_counter} {det_name} {qname}")
            self.probe_counter += 1

    # -------------------- Run --------------------
    def _append_run(self) -> None:
        """Append run section"""
        beam = self.data.get("beam", {})
        self.lines.extend([
            "\n##########################################",
            "################## Run ###################",
            "##########################################\n",
            f"/run/beamOn {beam.get('numberOfParticles', 10000)}\n"
        ])

    # -------------------- Results --------------------
    def _append_results(self) -> None:
        """Append results section"""
        detectors = {d["uuid"]: d for d in self.data.get("detectorManager", {}).get("detectors", [])}
        outputs = self.data.get("scoringManager", {}).get("outputs", [])

        self.lines.extend([
            "##########################################",
            "############ Collect results #############",
            "##########################################\n"
        ])

        for output in outputs:
            detector_uuid = output.get("detectorUuid")
            detector = detectors.get(detector_uuid)
            if not detector:
                continue
            name = utils.get_detector_name(detector)
            for quantity in output.get("quantities", []):
                qname = quantity.get("name", quantity.get("keyword", "UnknownQuantity"))
                filename = f"{name}_{qname}.txt"
                self.lines.append(f"/score/dumpQuantityToFile {name} {qname} {filename}")
