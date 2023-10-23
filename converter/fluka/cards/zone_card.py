from dataclasses import dataclass, field
from converter.fluka.helper_parsers.zone_parser import BoolOperation, FlukaRegion


@dataclass
class ZonesCard:
    """Class representing description of zones in Fluka input"""
    data: list[FlukaRegion] = field(default_factory=lambda: [])

    def __str__(self) -> str:
        """Return the card as a string."""
        result = ""
        for index, region in enumerate(self.data):
            if index == 0:
                line = ""
            else:
                line = "\n"
            line += "{} 5".format(region.name)
            # The '5' is the NAZ value for the region
            # From Fluka documentation:
            # NAZ is a rough guess for the number of regions which can be entered
            # leaving the current region, normally 5
            for zone_index, zone in enumerate(region.figures_operators):
                for operation, figure_name in zone:
                    if operation==BoolOperation.INTERSECTION:
                        line+=" +{}".format(figure_name)
                    elif operation==BoolOperation.SUBTRACTION:
                        line+=" -{}".format(figure_name)
                    if len(line>=120):
                        result+=line
                        line = "\n"
                if zone_index<len(region.figures_operators)-1:
                    line+=" |"

        return result