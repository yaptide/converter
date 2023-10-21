from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Class mapping of the beam.dat config file."""

    energy: float = 150.  # [MeV]
    num_histories: int = 100

    config_template: str = """s:Ge/MyBox/Type     = "TsBox"
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
d:So/Demo/BeamEnergy = {energy} MeV
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
i:So/Demo/NumberOfHistoriesInRun = {num_histories}
i:Ts/ShowHistoryCountAtInterval = {histories_interval}

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

    def __str__(self) -> str:
        """Return the topas_config.txt config file as a string."""
        result = self.config_template.format(
            energy=float(self.energy),
            num_histories=self.num_histories,
            histories_interval=max(1, self.num_histories//100)
        )

        return result
