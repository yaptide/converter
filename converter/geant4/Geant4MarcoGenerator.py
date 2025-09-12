from typing import Dict, Any, List

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
        self.data = data

    def generate(self) -> str:
        lines: List[str] = []

        # ===========================
        # Run initializaition
        # ===========================
        lines.append("/run/initialize\n")
        lines.append("##########################################")
        lines.append("####### Particle Source definition #######")
        lines.append("##########################################\n")

        beam = self.data.get("beam", {})
        particle = beam.get("particle", {}).get("name", "proton")
        pos = beam.get("position", [0, 0, 0])
        direction = beam.get("direction", [0, 0, 1])
        energy = beam.get("energy", 150)
        sigma = beam.get("energySpread", 0)
        energy_high = beam.get("energyHighCutoff", 1000)

        lines.append("/gps/verbose 0")
        lines.append(f"/gps/particle {particle.lower()}")
        lines.append(f"/gps/position {pos[0]} {pos[1]} {pos[2]} cm")
        lines.append("/gps/pos/type Beam")
        lines.append(f"/gps/direction {direction[0]} {direction[1]} {direction[2]}")
        lines.append("/gps/ene/type Gauss")
        lines.append(f"/gps/ene/mono {energy} MeV")
        lines.append(f"/gps/ene/sigma {sigma} MeV")
        lines.append(f"/gps/ene/max {energy_high} MeV\n")

        # ===========================
        # Scoring
        # ===========================
        lines.append("##########################################")
        lines.append("################ Scoring #################")
        lines.append("##########################################\n")

        detectors = {d["uuid"]: d for d in self.data.get("detectorManager", {}).get("detectors", [])}
        outputs = self.data.get("scoringManager", {}).get("outputs", [])
        filters = {f["uuid"]: f for f in self.data.get("scoringManager", {}).get("filters", [])}

        detector_quantities: Dict[str, List[Dict[str, Any]]] = {}
        for output in outputs:
            detector_uuid = output.get("detectorUuid")
            detector_quantities.setdefault(detector_uuid, []).extend(output.get("quantities", []))

        probe_histograms: List[Dict[str, Any]] = []
        probe_counter = 0

        for detector_uuid, quantities in detector_quantities.items():
            detector = detectors.get(detector_uuid)
            if not detector:
                continue

            name = detector.get("name", "UnknownDetector")
            geom = detector.get("geometryData", {})
            geom_type = geom.get("geometryType", "Box")
            params = geom.get("parameters", {})
            pos_det = geom.get("position", [0, 0, 0])

            is_probe = any(q.get("keyword") == "KineticEnergySpectrum" for q in quantities)
            if is_probe:
                if geom_type.lower() in ["cyl", "cylinder"]:
                    size = params.get("radius", 1)
                else:
                    size = max(params.get("width", 1), params.get("height", 1), params.get("depth", 1))
                lines.append(f"/score/create/probe {name} {size} cm")
                lines.append(f"/score/probe/locate {pos_det[0]} {pos_det[1]} {pos_det[2]} cm")
            else:
                if geom_type.lower() in ["cyl", "cylinder"]:
                    lines.append(f"/score/create/cylinderMesh {name}")
                    lines.append(f"/score/mesh/locate {pos_det[0]} {pos_det[1]} {pos_det[2]} cm")
                    radius = params.get("radius", 1)
                    depth = params.get("depth", 1)
                    n_radial = params.get("radialSegments", 1)
                    n_z = params.get("zSegments", 1)
                    lines.append(f"/score/mesh/cylinderSize {radius} {depth} cm")
                    lines.append(f"/score/mesh/nBin {n_radial} {n_z} 1")
                else:
                    lines.append(f"/score/create/boxMesh {name}")
                    lines.append(f"/score/mesh/locate {pos_det[0]} {pos_det[1]} {pos_det[2]} cm")
                    width = params.get("width", 1)
                    height = params.get("height", 1)
                    depth = params.get("depth", 1)
                    n_x = params.get("xSegments", 1)
                    n_y = params.get("ySegments", 1)
                    n_z = params.get("zSegments", 1)
                    lines.append(f"/score/mesh/boxSize {width} {height} {depth} cm")
                    lines.append(f"/score/mesh/nBin {n_x} {n_y} {n_z}")

            for quantity in quantities:
                keyword = quantity.get("keyword", "")
                qname = quantity.get("name", keyword)
                mapped_keyword = GEANT4_QUANTITY_MAP.get(keyword, keyword.lower())
                lines.append(f"/score/quantity/{mapped_keyword} {qname}")
                if keyword == "KineticEnergySpectrum":
                    probe_histograms.append({
                        "quantity": qname,
                        "detector": name,
                        "bins": quantity.get("histogramNBins", 1),
                        "min": quantity.get("histogramMin", 1),
                        "max": quantity.get("histogramMax", 1),
                        "unit": quantity.get("histogramUnit", "MeV")
                    })

                filter_uuid = quantity.get("filter")
                if filter_uuid and filter_uuid in filters:
                    filt = filters[filter_uuid]
                    particle_types = filt.get("data", {}).get("particleTypes", [])
                    if particle_types:
                        pt_names = " ".join([GEANT4_PARTICLE_MAP.get(pt["id"], pt["name"]) for pt in particle_types])
                        lines.append(f"/score/filter/particle {filt['name']} {pt_names}")

            lines.append("/score/close\n")


        for hist in probe_histograms:
            qname = hist["quantity"]
            det_name = hist["detector"]
            arbitrary_name = f"{qname}_differential_{probe_counter}"
            lines.append(f"/analysis/h1/create {qname} {arbitrary_name} {hist['bins']} {hist['min']} {hist['max']} {hist['unit']}")
            lines.append(f"/score/fill1D {probe_counter} {det_name} {qname}")
            probe_counter += 1

        # ===========================
        # Run beam
        # ===========================
        lines.append("\n##########################################")
        lines.append("################## Run ###################")
        lines.append("##########################################\n")
        lines.append(f"/run/beamOn {beam.get('numberOfParticles', 10000)}\n")

        # ===========================
        # Collect results
        # ============================
        lines.append("##########################################")
        lines.append("############ Collect results #############")
        lines.append("##########################################\n")
        for output in outputs:
            detector_uuid = output.get("detectorUuid")
            detector = detectors.get(detector_uuid)
            if not detector:
                continue
            name = detector.get("name", "UnknownDetector")
            for quantity in output.get("quantities", []):
                qname = quantity.get("name", quantity.get("keyword", "UnknownQuantity"))
                filename = f"{name}_{qname}.txt"
                lines.append(f"/score/dumpQuantityToFile {name} {qname} {filename}")

        return "\n".join(lines)