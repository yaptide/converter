from dataclasses import dataclass

@dataclass
class USRBIN():
    name: str
    x_min: float
    x_max: float
    x_bins: int
    y_min: float
    y_max: float
    y_bins: int
    z_min: float
    z_max: float
    z_bins: int

def parse_detector(detectors_json: dict, detectorUuid: str) -> USRBIN:

    for detector in detectors_json['detectors']:
        if detector['uuid'] == detectorUuid:
            return USRBIN(
                name=detector['name'],

            )
