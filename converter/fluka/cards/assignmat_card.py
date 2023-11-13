from dataclasses import dataclass, field
from converter.fluka.cards.card import Card

@dataclass
class AssignMatCard(Card):
    """
    Class representing description of material assignment in FLUKA input.
    Card consists of:
    - codewd (str): 'ASSIGNMA'
    - what (list[str]): list of parameters (see FLUKA manual for details)
    sdum is not used.
    """
    
    codewd: str = "ASSIGNMA"
    region_name: str = ""
    material_name: str = "BLCKHOLE"

    def __post_init__(self) -> None:
        """Set material and region on appropriate positions in what list."""
        super().__post_init__()
        self.what[0] = self.material_name
        self.what[1] = self.region_name 
