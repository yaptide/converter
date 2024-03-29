"""Pre-defined single-element FLUKA materials"""
PREDEFINED_MATERIALS = [
    {
        "fluka_name": "BLCKHOLE",
        "fluka_number": 1,
        "common_name": "Blackhole or External Vacuum",
        "A": 0,
        "Z": 0,
        "density": 0,
        "icru": 0,
    },
    {
        "fluka_name": "VACUUM",
        "fluka_number": 2,
        "common_name": "Vacuum or Internal Vacuum",
        "A": 0,
        "Z": 0,
        "density": 0,
        "icru": 1000,
    },
    {
        "fluka_name": "HYDROGEN",
        "fluka_number": 3,
        "common_name": "Hydrogen",
        "A": 1.00794,
        "Z": 1,
        "density": 0.0000837,
        "icru": 1,
    },
    {
        "fluka_name": "HELIUM",
        "fluka_number": 4,
        "common_name": "Helium",
        "A": 4.002602,
        "Z": 2,
        "density": 0.000166,
        "icru": 2,
    },
    {
        "fluka_name": "BERYLLIU",
        "fluka_number": 5,
        "common_name": "Beryllium",
        "A": 9.012182,
        "Z": 4,
        "density": 1.848,
        "icru": 4,
    },
    {
        "fluka_name": "CARBON",
        "fluka_number": 6,
        "common_name": "Carbon",
        "A": 12.0107,
        "Z": 6,
        "density": 2.000,
        "icru": 6,
    },
    {
        "fluka_name": "NITROGEN",
        "fluka_number": 7,
        "common_name": "Nitrogen",
        "A": 14.0067,
        "Z": 7,
        "density": 0.00117,
        "icru": 7,
    },
    {
        "fluka_name": "OXYGEN",
        "fluka_number": 8,
        "common_name": "Oxygen",
        "A": 15.9994,
        "Z": 8,
        "density": 0.00133,
        "icru": 8,
    },
    {
        "fluka_name": "MAGNESIU",
        "fluka_number": 9,
        "common_name": "Magnesium",
        "A": 24.3050,
        "Z": 12,
        "density": 1.740,
        "icru": 12,
    },
    {
        "fluka_name": "ALUMINUM",
        "fluka_number": 10,
        "common_name": "Aluminium",
        "A": 26.981538,
        "Z": 13,
        "density": 2.699,
        "icru": 13,
    },
    {
        "fluka_name": "IRON",
        "fluka_number": 11,
        "common_name": "Iron",
        "A": 55.845,
        "Z": 26,
        "density": 7.874,
        "icru": 26,
    },
    {
        "fluka_name": "COPPER",
        "fluka_number": 12,
        "common_name": "Copper",
        "A": 63.546,
        "Z": 29,
        "density": 8.960,
        "icru": 29,
    },
    {
        "fluka_name": "SILVER",
        "fluka_number": 13,
        "common_name": "Silver",
        "A": 107.8682,
        "Z": 47,
        "density": 10.500,
        "icru": 47,
    },
    {
        "fluka_name": "SILICON",
        "fluka_number": 14,
        "common_name": "Silicon",
        "A": 28.0855,
        "Z": 14,
        "density": 2.329,
        "icru": 14,
    },
    {
        "fluka_name": "GOLD",
        "fluka_number": 15,
        "common_name": "Gold",
        "A": 196.96655,
        "Z": 79,
        "density": 19.320,
        "icru": 79,
    },
    {
        "fluka_name": "MERCURY",
        "fluka_number": 16,
        "common_name": "Mercury",
        "A": 200.59,
        "Z": 80,
        "density": 13.546,
        "icru": 80,
    },
    {
        "fluka_name": "LEAD",
        "fluka_number": 17,
        "common_name": "Lead",
        "A": 207.2,
        "Z": 82,
        "density": 11.350,
        "icru": 82,
    },
    {
        "fluka_name": "TANTALUM",
        "fluka_number": 18,
        "common_name": "Tantalum",
        "A": 180.9479,
        "Z": 73,
        "density": 16.654,
        "icru": 73,
    },
    {
        "fluka_name": "SODIUM",
        "fluka_number": 19,
        "common_name": "Sodium",
        "A": 22.989770,
        "Z": 11,
        "density": 0.971,
        "icru": 11,
    },
    {
        "fluka_name": "ARGON",
        "fluka_number": 20,
        "common_name": "Argon",
        "A": 39.948,
        "Z": 18,
        "density": 0.00166,
        "icru": 18,
    },
    {
        "fluka_name": "CALCIUM",
        "fluka_number": 21,
        "common_name": "Calcium",
        "A": 40.078,
        "Z": 20,
        "density": 1.550,
        "icru": 20,
    },
    {
        "fluka_name": "TIN",
        "fluka_number": 22,
        "common_name": "Tin",
        "A": 118.710,
        "Z": 50,
        "density": 7.310,
        "icru": 50,
    },
    {
        "fluka_name": "TUNGSTEN",
        "fluka_number": 23,
        "common_name": "Tungsten",
        "A": 183.84,
        "Z": 74,
        "density": 19.300,
        "icru": 74,
    },
    {
        "fluka_name": "TITANIUM",
        "fluka_number": 24,
        "common_name": "Titanium",
        "A": 47.867,
        "Z": 22,
        "density": 4.540,
        "icru": 22,
    },
    {
        "fluka_name": "NICKEL",
        "fluka_number": 25,
        "common_name": "Nickel",
        "A": 58.6934,
        "Z": 28,
        "density": 8.902,
        "icru": 28,
    },
]
"""Fluka names for ICRU single-particles"""
FLUKA_NAMES = [
    {
        "fluka_name": "HYDROGEN",
        "icru": 1
    },
    {
        "fluka_name": "HELIUM",
        "icru": 2
    },
    {
        "fluka_name": "LITHIUM",
        "icru": 3
    },
    {
        "fluka_name": "BERYLLIU",
        "icru": 4
    },
    {
        "fluka_name": "BORON",
        "icru": 5
    },
    {
        "fluka_name": "CARBON",
        "icru": 6
    },
    {
        "fluka_name": "NITROGEN",
        "icru": 7
    },
    {
        "fluka_name": "OXYGEN",
        "icru": 8
    },
    {
        "fluka_name": "FLUORINE",
        "icru": 9
    },
    {
        "fluka_name": "NEON",
        "icru": 10
    },
    {
        "fluka_name": "SODIUM",
        "icru": 11
    },
    {
        "fluka_name": "MAGNESIU",
        "icru": 12
    },
    {
        "fluka_name": "ALUMINUM",
        "icru": 13
    },
    {
        "fluka_name": "SILICON",
        "icru": 14
    },
    {
        "fluka_name": "PHOSPHO",
        "icru": 15
    },
    {
        "fluka_name": "SULFUR",
        "icru": 16
    },
    {
        "fluka_name": "CHLORINE",
        "icru": 17
    },
    {
        "fluka_name": "ARGON",
        "icru": 18
    },
    {
        "fluka_name": "POTASSIU",
        "icru": 19
    },
    {
        "fluka_name": "CALCIUM",
        "icru": 20
    },
    {
        "fluka_name": "SCANDIUM",
        "icru": 21
    },
    {
        "fluka_name": "TITANIUM",
        "icru": 22
    },
    {
        "fluka_name": "VANADIUM",
        "icru": 23
    },
    {
        "fluka_name": "CHROMIUM",
        "icru": 24
    },
    {
        "fluka_name": "MANGANES",
        "icru": 25
    },
    {
        "fluka_name": "IRON",
        "icru": 26
    },
    {
        "fluka_name": "COBALT",
        "icru": 27
    },
    {
        "fluka_name": "NICKEL",
        "icru": 28
    },
    {
        "fluka_name": "COPPER",
        "icru": 29
    },
    {
        "fluka_name": "ZINC",
        "icru": 30
    },
    {
        "fluka_name": "GALLIUM",
        "icru": 31
    },
    {
        "fluka_name": "GERMANIU",
        "icru": 32
    },
    {
        "fluka_name": "ARSENIC",
        "icru": 33
    },
    {
        "fluka_name": "BROMINE",
        "icru": 35
    },
    {
        "fluka_name": "KRYPTON",
        "icru": 36
    },
    {
        "fluka_name": "STRONTIU",
        "icru": 38
    },
    {
        "fluka_name": "YTTRIUM",
        "icru": 39
    },
    {
        "fluka_name": "ZIRCONIU",
        "icru": 40
    },
    {
        "fluka_name": "NIOBIUM",
        "icru": 41
    },
    {
        "fluka_name": "MOLYBDEN",
        "icru": 42
    },
    {
        "fluka_name": "99-TC",
        "icru": 43
    },
    {
        "fluka_name": "PALLADIU",
        "icru": 46
    },
    {
        "fluka_name": "SILVER",
        "icru": 47
    },
    {
        "fluka_name": "CADMIUM",
        "icru": 48
    },
    {
        "fluka_name": "INDIUM",
        "icru": 49
    },
    {
        "fluka_name": "TIN",
        "icru": 50
    },
    {
        "fluka_name": "ANTIMONY",
        "icru": 51
    },
    {
        "fluka_name": "IODINE",
        "icru": 53
    },
    {
        "fluka_name": "XENON",
        "icru": 54
    },
    {
        "fluka_name": "CESIUM",
        "icru": 55
    },
    {
        "fluka_name": "BARIUM",
        "icru": 56
    },
    {
        "fluka_name": "LANTHANU",
        "icru": 57
    },
    {
        "fluka_name": "CERIUM",
        "icru": 58
    },
    {
        "fluka_name": "NEODYMIU",
        "icru": 60
    },
    {
        "fluka_name": "SAMARIUM",
        "icru": 62
    },
    {
        "fluka_name": "EUROPIUM",
        "icru": 63
    },
    {
        "fluka_name": "GADOLINI",
        "icru": 64
    },
    {
        "fluka_name": "TERBIUM",
        "icru": 65
    },
    {
        "fluka_name": "LUTETIUM",
        "icru": 71
    },
    {
        "fluka_name": "HAFNIUM",
        "icru": 72
    },
    {
        "fluka_name": "TANTALUM",
        "icru": 73
    },
    {
        "fluka_name": "TUNGSTEN",
        "icru": 74
    },
    {
        "fluka_name": "RHENIUM",
        "icru": 75
    },
    {
        "fluka_name": "IRIDIUM",
        "icru": 77
    },
    {
        "fluka_name": "PLATINUM",
        "icru": 78
    },
    {
        "fluka_name": "GOLD",
        "icru": 79
    },
    {
        "fluka_name": "MERCURY",
        "icru": 80
    },
    {
        "fluka_name": "LEAD",
        "icru": 82
    },
    {
        "fluka_name": "BISMUTH",
        "icru": 83
    },
    {
        "fluka_name": "230-TH",
        "icru": 89
    },
    {
        "fluka_name": "233-U",
        "icru": 92
    },
    {
        "fluka_name": "239-PU",
        "icru": 94
    },
    {
        "fluka_name": "241-AM",
        "icru": 95
    },
]
"""Pre-defined FLUKA ICRU compounds"""
PREDEFINED_COMPOUNDS = [
    {
        "fluka_name": "WATER",
        "common_name": "Water",
        "density": 1.0,
        "icru": 276
    },
    {
        "fluka_name": "POLYSTYR",
        "common_name": "Polystyrene",
        "density": 1.06,
        "icru": 226,
    },
    {
        "fluka_name": "PLASCINT",
        "common_name": "Plastic scintillator",
        "density": 1.032,
        "icru": 216,
    },
    {
        "fluka_name": "PMMA",
        "common_name": "Polymethyl methacrylate, Plexiglas, Lucite, Perspex",
        "density": 1.19,
        "icru": 223,
    },
    {
        "fluka_name": "BONECOMP",
        "common_name": "Compact bone",
        "density": 1.85,
        "icru": 119,
    },
    {
        "fluka_name": "BONECORT",
        "common_name": "Cortical bone",
        "density": 1.85,
        "icru": 120,
    },
    {
        "fluka_name": "MUSCLESK",
        "common_name": "Skeletal muscle",
        "density": 1.04,
        "icru": 201,
    },
    {
        "fluka_name": "MUSCLEST",
        "common_name": "Striated muscle",
        "density": 1.04,
        "icru": 202,
    },
    {
        "fluka_name": "ADTISSUE",
        "common_name": "Adipose tissue",
        "density": 0.92,
        "icru": 103,
    },
    {
        "fluka_name": "KAPTON",
        "common_name": "Kapton polyimide film",
        "density": 1.42,
        "icru": 179,
    },
    {
        "fluka_name": "POLYETHY",
        "common_name": "Polyethylene",
        "density": 0.94,
        "icru": 221,
    },
    {
        "fluka_name": "AIR",
        "common_name": "Dry air at NTP conditions",
        "density": 0.00120479,
        "icru": 104,
    },
]
