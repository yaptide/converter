from functools import reduce


class BeamConfig:
    energy: float
    nstat: int

    def __init__(self, energy: float, nstat: int):
        self.energy = energy
        self.nstat = nstat

    def set_energy(self, energy: float) -> None:
        self.energy = energy

    def set_nstat(self, nstat: int) -> None:
        self.nstat = nstat

    def __str__(self) -> str:
        return """
        RNDSEED      	89736501     ! Random seed
        JPART0       	2            ! Incident particle type
        TMAX0      	{energy:3.6f}   0.0  ! Incident energy; (MeV/nucl)
        NSTAT       {nstat:d}    -1 ! NSTAT, Step of saving
        STRAGG          2            ! Straggling: 0-Off 1-Gauss, 2-Vavilov
        MSCAT           2            ! Mult. scatt 0-Off 1-Gauss, 2-Moliere
        NUCRE           0            ! Nucl.Reac. switcher: 1-ON, 0-OFF
        """.format(energy=self.energy, nstat=self.nstat)


class MatConfig:
    materials: list[int]

    def __init__(self):
        self.materials = []

    def add_materials(self, *materials_to_add: int) -> list[int]:
        self.materials += list(materials_to_add)
        return self.materials

    def remove_materials(self, *materials_to_remove) -> list[int]:
        self.materials = list(
            filter(lambda mat: mat not in materials_to_remove, self.materials))
        return self.materials

    def clear_materials(self) -> None:
        self.materials = []

    def get_materials(self) -> list[int]:
        return self.materials

    def __str__(self) -> str:
        material_strings = map((lambda mat, idx: """MEDIUM {idx}
        ICRU {mat}
        END
        """.format(idx=idx+1, mat=mat)), self.materials, list(range(len(self.materials))))
        return reduce((lambda acc, str: acc + str), material_strings, initializer="\n")


class DetectConfig:
    pass


class GeoConfig:
    pass
