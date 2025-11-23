GEANT4_PARTICLE_MAP = {
    1: {
        "name": "neutron",
        "allowed_units": ["MeV", "MeV/nucl"],
        "target_unit": "MeV"
    },
    2: {
        "name": "proton",
        "allowed_units": ["MeV", "MeV/nucl"],
        "target_unit": "MeV"
    },
    3: {
        "name": "geantino",
        "allowed_units": ["MeV"],
        "target_unit": "MeV"
    },
    4: {
        "name": "e-",
        "allowed_units": ["MeV"],
        "target_unit": "MeV"
    },
    5: {
        "name": "e+",
        "allowed_units": ["MeV"],
        "target_unit": "MeV"
    },
    6: {
        "name": "alpha",
        "allowed_units": ["MeV", "MeV/nucl"],
        "target_unit": "MeV"
    },
    7: {
        "name": "mu-",
        "allowed_units": ["MeV"],
        "target_unit": "MeV"
    },
    8: {
        "name": "mu+",
        "allowed_units": ["MeV"],
        "target_unit": "MeV"
    },
    9: {
        "name": "pi-",
        "allowed_units": ["MeV"],
        "target_unit": "MeV"
    },
    10: {
        "name": "pi+",
        "allowed_units": ["MeV"],
        "target_unit": "MeV"
    },
    11: {
        "name": "geantino",
        "allowed_units": ["MeV"],
        "target_unit": "MeV"
    },
    25: {  # equivalent of HEAVYION in other simulators
        "name": "ion",
        "allowed_units": ["MeV", "MeV/nucl"],
        "target_unit": "MeV"
    }
}

GEANT4_QUANTITY_MAP = {
    "DoseGy": "doseDeposit",
    "Energy": "energyDeposit",
    "Fluence": "cellFlux",
    "KineticEnergySpectrum": "cellFlux",
}

GEANT4_KINETIC_ENERGY_SPECTRUM = "KineticEnergySpectrum"

HEAVY_ION_PARTICLE_ID = 25