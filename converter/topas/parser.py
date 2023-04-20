from converter.common import Parser
from pathlib import Path

DEFAULT_CONFIG = """s:Ge/MyBox/Type     = "TsBox"
s:Ge/MyBox/Material = "Air"
s:Ge/MyBox/Parent   = "World"
d:Ge/MyBox/HLX      = 2.5 m
d:Ge/MyBox/HLY      = 2. m
d:Ge/MyBox/HLZ      = 1. m
d:Ge/MyBox/TransX   = 2. m
d:Ge/MyBox/TransY   = 0. m
d:Ge/MyBox/TransZ   = 0. m
d:Ge/MyBox/RotX     = 0. deg
d:Ge/MyBox/RotY     = 0. deg
d:Ge/MyBox/RotZ     = 0. deg

s:So/Demo/Type = "Beam"
s:So/Demo/Component = "BeamPosition"
s:So/Demo/BeamParticle = "proton"
d:So/Demo/BeamEnergy = 169.23 MeV
u:So/Demo/BeamEnergySpread = 0.757504
s:So/Demo/BeamPositionDistribution = "Gaussian"
s:So/Demo/BeamPositionCutoffShape = "Ellipse"
d:So/Demo/BeamPositionCutoffX = 10. cm
d:So/Demo/BeamPositionCutoffY = 10. cm
d:So/Demo/BeamPositionSpreadX = 0.65 cm
d:So/Demo/BeamPositionSpreadY = 0.65 cm
s:So/Demo/BeamAngularDistribution = "Gaussian"
d:So/Demo/BeamAngularCutoffX = 90. deg
d:So/Demo/BeamAngularCutoffY = 90. deg
d:So/Demo/BeamAngularSpreadX = 0.0032 rad
d:So/Demo/BeamAngularSpreadY = 0.0032 rad
i:So/Demo/NumberOfHistoriesInRun = 10

s:Ge/BeamPosition/Parent="World"
s:Ge/BeamPosition/Type="Group"
d:Ge/BeamPosition/TransX=0. m
d:Ge/BeamPosition/TransY=0. m
d:Ge/BeamPosition/TransZ= Ge/World/HLZ m
d:Ge/BeamPosition/RotX=180. deg
d:Ge/BeamPosition/RotY=0. deg
d:Ge/BeamPosition/RotZ=0. deg

s:Sc/Dose/Quantity                  = "DoseToWater"
s:Sc/Dose/Component                 = "WaterPhantom"
s:Sc/Dose/IfOutputFileAlreadyExists = "Overwrite"
s:Sc/Dose/OutputType                = "CSV"

s:Ge/WaterPhantom/Parent            = "MyBox"
s:Ge/WaterPhantom/Type              = "TsBox"
s:Ge/WaterPhantom/Material          = "G4_WATER"
d:Ge/WaterPhantom/HLX               = 2.5 m
d:Ge/WaterPhantom/HLY               = 2. m
d:Ge/WaterPhantom/HLZ               = 0.1 cm
i:Ge/WaterPhantom/XBins             = 80
i:Ge/WaterPhantom/YBins             = 80
i:Ge/WaterPhantom/ZBins             = 1
d:Ge/WaterPhantom/TransZ            = 0. cm
s:Ge/WaterPhantom/DrawingStyle      = "Solid"
s:Ge/WaterPhantom/Color             = "skyblue"

sv:Ph/Default/Modules = 1 "g4em-standard_opt0"
"""


class TopasParser(Parser):
    """A simple placeholder parser that ignores the json input and prints example (default) configs."""

    def __init__(self) -> None:
        super().__init__()
        version = "unknown"
        self.info = {
            "version": version,
            "label": "development",
            "simulator": "topas",
        }

    def parse_configs(self, json: dict) -> None:
        """Basicaly do nothing since we work on defaults in this parser."""

    def save_configs(self, target_dir: str) -> None:
        """Save the configs as text files in the target_dir in file topas_config.txt."""
        if not Path(target_dir).exists():
            raise ValueError("Target directory does not exist.")

        for file_name, content in self.get_configs_json().items():
            with open(Path(target_dir, file_name), 'w') as conf_f:
                conf_f.write(content)

    def get_configs_json(self) -> dict:
        """
        Return a dict representation of the config files. Each element has
        the config files name as key and its content as value.
        """
        configs_json = {
            "topas_config.txt": DEFAULT_CONFIG
        }

        return configs_json
